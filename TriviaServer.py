import socket
import select
import json
import random
import os
import requests
from bs4 import BeautifulSoup
import bisect

# CONSTANTS
SERVER_IP = '0.0.0.0'
SERVER_PORT = 45122
MAX_MSG_LENGTH = 1024


def get_content(url):
    return requests.get(url).text


def extract_weather():
    print("fetching a new temperature")
    url = r"https://www.google.com/search?q=weather&rlz=1C1EJFA_enIL798IL813&oq=weather+&aqs=chrome..69i57j0j0i131i433j0l2.1799j0j7&sourceid=chrome&ie=UTF-8"
    html_content = get_content(url)
    soup = BeautifulSoup(html_content, features="lxml")
    tags = soup.find_all("div", {"class": "BNeawe iBp4i AP7Wnd"})[1]
    span_tag = tags.findChild("span", recursive=False)
    return span_tag.text


def create_server():
    """ Creating the server """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    return server_socket


# ************************* *HANDLING TRIVIA JSON RELATED JSON FILES: QUESTIONS & LEADERBOARD **************************

def extract_content():
    """ Gets the questions in form of lists and dictionaries from the json text file """
    with open('final_questions.json') as q_file:
        content = q_file.read()
        questions = json.loads(content)
        return questions


# GLOBAL VARIABLE FOR THE QUESTIONS ( SAVES TIME INSTEAD OF RETRIEVING DATA EVERY TIME )


QUESTIONS = extract_content()


def get_question(questions):
    random_index = random.randrange(0, len(questions["results"]))
    return questions['results'][random_index]


def print_client_sockets(client_sockets):
    """ Printing the clients socket """
    for client in client_sockets:
        print("\t", client.getpeername())


def get_leaderboard():
    """
    fetch the leaderboard from the leaderboard.txt file
    """
    with open("leaderboard.txt") as json_scores:
        scores = []
        for json_score in json_scores.readlines():
            scores.append(json_score.replace("\n", ""))
        return json.dumps(scores)


def get_average():
    """ fetch the average rating """
    ratings_sum = 0
    counter = 0
    with open("ratings.txt") as ratings_file:
        for json_obj in ratings_file.readlines():
            ratings_sum += float(json.loads(json_obj)["rating"])
            counter += 1
        if counter == 0:
            return "No Votes"
        return round(ratings_sum / counter, 2)


def get_place(score):
    """gets the place in the leaderboard """
    with open("leaderboard.txt") as json_scores:
        scores = json_scores.readlines()
        if os.stat("leaderboard.txt").st_size == 0:
            return 0

        for index, json_obj in enumerate(scores):
            if score > int(json.loads(json_obj)["score"]):
                return index
    return len(scores)


def add_to_leaderboard(player):
    """ add a player to the leaderboard """
    player = player.strip()
    print(player)
    player_obj = json.loads(player)
    player_place = get_place(player_obj["score"])
    if player_place < 11:
        content = ""
        with open("leaderboard.txt", 'rt') as file:
            content = file.readlines()
        content.insert(player_place, f'{player}\n')
        if len(content) > 10:
            content.pop()
        with open("leaderboard.txt", 'w') as json_data:
            json_data.write("".join(content))


# ************************************************ HANDLING USERS FOR GUI *********************************************

def get_users_data():
    with open('users.json', 'r') as users_file:
        return f'{users_file.read()}'


def add_to_users(user_json):
    print("adding to users ...")
    with open('users.json', 'r') as users_file:
        content = get_users_data()
        if get_users_data() == "":
            print("empty")
            users = [json.loads(rf'{user_json}')]
        else:
            print(f"the content is {content}")
            users = json.loads(content)
            # user_json.replace('"',"")
            # user_json.replace()
            users.append(json.loads(user_json))
            print(f"users is {users}")
    with open('users.json', 'w') as users_file:
        users_file.write(json.dumps(users, indent=4))


def fetch_users():
    """ retrieves all the users_json """
    with open("users.json") as users_file:
        users = json.loads(users_file.read())
    return users


def update_users(users_objects):
    """ updates the users json by the new objects values """
    with open("users.json", 'w') as users_file:
        new_users_json = json.dumps(users_objects, indent=4)
        users_file.write(new_users_json)


def get_user_index_by_name(user_name):
    """Gets the user index by the user_name"""
    users = fetch_users()
    for index, user_dict in enumerate(users):
        if user_dict["_User__user_name"] == user_name:
            return users, index
    return None


def replace(user_obj):
    users_objects = fetch_users()
    replacement_index = -1
    for index, user_object in enumerate(users_objects):
        if user_obj['_User__user_name'] == user_object['_User__user_name'] and user_obj['_User__email'] == user_object[
            '_User__email']:  # double authentication
            replacement_index = index
            break
    if replacement_index == -1:
        return False  # Failure - user does not exist !
    print(f"replacement index is {replacement_index}")
    users_objects[replacement_index] = user_obj
    update_users(users_objects)


def verify_user(email, password):
    """ checks if the login details match any of the existing users"""
    print(f"the email is {email}, and the password is {password}")
    with open('users.json') as users_file:
        users = json.loads(users_file.read())
    print(len(users))
    for user_obj in users:
        print(f'{email} == {user_obj["_User__email"]} : {email == user_obj["_User__email"]}')
        print(f'{password} == {user_obj["_User__password"]} : {password == user_obj["_User__password"]}')
        if user_obj["_User__email"].strip() == email.strip() and user_obj[
            "_User__password"].strip() == password.strip():
            print(f"found a match ! sending {user_obj}")
            user_json = json.dumps(user_obj, indent=4)
            print("adding to the online users")
            add_to_online(user_obj)
            return user_json
    print("returning none...")
    return None


def add_to_online(user_obj):
    """ Adds the user to the online users file, so no one else can enter his account while he is online"""
    with open('online.json', 'r') as online_users:
        current_online = json.loads(online_users.read())
    current_online.append(user_obj)
    with open("online.json", 'w') as online_users:
        online_users.write(json.dumps(current_online, indent=4))


def remove_from_online(user_obj):
    with open('online.json', 'r') as online_users:
        current_online = json.loads(online_users.read())

    current_online.remove(user_obj)
    print(f"{user_obj['_User__user_name']} is offline !")
    with open("online.json", 'w') as online_users:
        online_users.write(json.dumps(current_online, indent=4))


def check_user_taken(user_name, email, password):
    with open('users.json') as users_file:
        users = json.loads(users_file.read())
    print(F"USER NAME IS {user_name}, EMAIL IS {email} AND PASSWORD IS {password} ")
    for user_obj in users:
        if user_obj["_User__user_name"].strip() == user_name.strip():
            return "1"  # 1 will signal to the client that the user is taken
        elif user_obj["_User__email"].strip() == email.strip():
            return "2"  # email address is taken
        elif user_obj["_User__password"].strip() == password:
            return "3"  # password is taken
    return "0"  # all is fine, the user is not in the system !


# **************************************************** MAIN **********************************************************


def main():
    server_socket = create_server()
    server_socket.listen()
    print("Listening for clients. ...")
    client_sockets = []
    messages_to_send = []
    tic_tac_toe_waiting = []
    tic_tac_toe_playing = []
    running = True
    while running:
        read_list = [server_socket] + client_sockets
        write_list = client_sockets
        rlist, wlist, xlist = select.select(read_list, write_list, [])
        for current_socket in rlist:
            if current_socket is server_socket:  # from server -> new client is joining
                connection, client_address = current_socket.accept()
                print("New client has joined!")
                client_sockets.append(connection)  # append the socket to the clients list
            else:
                data = current_socket.recv(MAX_MSG_LENGTH).decode()
                if data == "quit":  # closing the connection if the client sends "quit"
                    print("connection closed")
                    client_sockets.remove(current_socket)  # removing the client from the client list
                    current_socket.close()  # closing the socket
                else:
                    if data == 'question':  # If it's a query for a trivia question
                        json_question = get_question(QUESTIONS)
                        # print(f'{type(messages_to_send)} in questions')
                        messages_to_send.append((current_socket, str(json_question)))
                        # print(f'{type(messages_to_send)} in questions')
                    elif "leader" in data.strip():
                        print("fetching leaderboard...")
                        messages_to_send.append((current_socket, str(get_leaderboard())))
                        # print(f'{type(messages_to_send)} in leader')
                    elif data.startswith("add"):
                        q = data[data.index("{"):data.rindex("}") + 1]
                        add_to_leaderboard(q)
                        print("added to leaderboard")
                    elif data == "weather":
                        print("the weather has been requested !")
                        temperature = extract_weather()
                        messages_to_send.append((current_socket, temperature))
                        print(f"sent {temperature}")
                    elif data.startswith("rate"):
                        data = data[data.index("{"):data.rindex("}") + 1]
                        data = data.replace("rate", "")
                        print(f"received {data}")
                        with open("ratings.txt", "a") as ratings_file:
                            ratings_file.write(f"{data}\n")
                    elif data == "avg":
                        messages_to_send.append((current_socket, str(get_average())))
                    elif data.startswith("user"):  # register
                        data = data[data.index("{"):data.rindex("}") + 1]
                        user_obj = json.loads(data)
                        is_user_taken = check_user_taken(user_obj["_User__user_name"], user_obj["_User__email"],
                                                         user_obj["_User__password"])
                        if is_user_taken == "0":
                            add_to_users(data)
                        messages_to_send.append((current_socket, is_user_taken))
                    elif data.startswith("verify"):  # login
                        data = data[data.index("[") + 1:data.rindex("]")]
                        email, password = data.strip().split(',')
                        email, password = email[email.index("(") + 1:], password[:password.index(")")]
                        email, password = email[email.index("'") + 1:email.rindex("'")], password[
                                                                                         password.index(
                                                                                             "'") + 1:password.rindex(
                                                                                             "'")]
                        verification = verify_user(email=email, password=password)
                        message = "0" if verification is None else verification  # if the user is found, send the user
                        # else , send "0"
                        messages_to_send.append((current_socket, message))
                    elif data.startswith('logout'):
                        user_to_remove = data[data.index("{"):data.index("}") + 1]
                        user_obj = json.loads(user_to_remove)
                        remove_from_online(user_obj)
                    elif data.startswith("<tictac>") or "<tictac>" in data:
                        print("New client in tic tac toe")
                        # meaning: a client wishes to play multiplayer tic tac toe.
                        tic_tac_toe_waiting.append(current_socket)  # ADD THE SOCKET TO THE WAITING LIST.
                        if len(tic_tac_toe_waiting) == 2:
                            print("the game should start!")
                            tic_tac_toe_waiting[0].send(str("x").encode())
                            tic_tac_toe_waiting[1].send(str("o").encode())
                            # messages_to_send.append((tic_tac_toe_waiting[1], "o"))
                            # messages_to_send.append((tic_tac_toe_waiting[0], "x"))
                            tic_tac_toe_playing.append((tic_tac_toe_waiting[0], tic_tac_toe_waiting[1]))
                            tic_tac_toe_waiting = []
                    elif data.startswith("ticmove"):
                        place = data[7]
                        print(f"received {data}")
                        for x_player, o_player in tic_tac_toe_playing:
                            if current_socket is x_player:
                                print("x delivers a move")
                                o_player.send(str(place).encode())
                                # messages_to_send.append((o_player, place))
                                break
                            elif current_socket is o_player:
                                print("o delivers a move")
                                x_player.send(str(place).encode())
                                # messages_to_send.append((x_player, place))
                                break
                    elif data.startswith('replace'):
                        user_json = data[data.index('{'):data.index('}') + 1]
                        print(user_json)
                        user_obj = json.loads(user_json)
                        print(f"Replacing: {user_obj}")
                        replace(user_obj)
                    elif '*' in data:
                        data = data[data.index('*') + 1:data.rindex('*')]
                        purchase_index, user_name = data.split(',')
                        print(f'purchase index: {purchase_index}, user : {user_name}')

            for message in messages_to_send:  # sending to all clients in the write list, then removing from list
                current_socket, data = message
                if current_socket in wlist:
                    current_socket.send(str(data).encode())  # send them the data
                    messages_to_send.remove(message)


if __name__ == '__main__':
    main()
