from dotenv import load_dotenv
import os, base64, requests, json
import tkinter as tkn


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    header = {
        "Authorization":"Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type":"client_credentials"}

    result = requests.post(url, headers=header, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token
token = get_token()

def get_auth_headr(token):
    return {"Authorization":"Bearer " + token}

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    header = get_auth_headr(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = requests.get(query_url, headers=header)
    json_result = json.loads(result.content)
    if 'error' in json_result.keys():
        return "We have encountered an error ..."
    elif len(json_result['artists']['items']) == 0:
        return "There exists to be no artist with that name ..."
    else:
        return json_result['artists']

def get_top_songs_from_artist(token, artist_name):
    result_from_search = search_artist(token, artist_name)
    if isinstance(result_from_search, dict):
        artist_id = result_from_search['items'][0]['id']
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=CA"
        header = get_auth_headr(token)
        result = requests.get(url, headers=header)
        json_result = json.loads(result.content)['tracks']
        return json_result     
    else:
        return result_from_search

def formatted_n_top_songs_from_artist(token, artist_name, max):
    final_result = ""
    if isinstance(get_top_songs_from_artist(token, artist_name), list):
        top_songs = get_top_songs_from_artist(token, artist_name)
        for index in range(1,max+1):
            song_name = top_songs[index-1]['name']
            album_name = top_songs[index-1]['album']['name']
            song_id = top_songs[index-1]['id']
            song_url = f"https://open.spotify.com/album/{song_id}"
            if index == max:
                final_result += f"{index}. {song_name} \n   {album_name} \n   {song_url}"
            else:
                final_result += f"{index}. {song_name} \n   {album_name} \n   {song_url} \n\n"
        return final_result
    else:
        final_result = get_top_songs_from_artist(token, artist_name)
        return final_result

def how_many_top_songs_window(): 
    def top_songs_window():
        no_of_top_songs = int(entry_label_2.get())
        result_to_be_displayed = formatted_n_top_songs_from_artist(token,artist,no_of_top_songs)
        window_2.destroy()
        if "We have" in result_to_be_displayed:
            error_window(result_to_be_displayed)
        elif "There exists" in result_to_be_displayed:
            error_window(result_to_be_displayed)
        else:
            window_3 = tkn.Tk()
            window_3.geometry("650x650")
            window_3.resizable(width=False, height=False)
            frame = tkn.Frame(master=window_3)
            result = tkn.Label(master=window_3, text=result_to_be_displayed, height=41, width=96,anchor='center',font=("Helvetica", 8))
            result.place(x=33, y=20)
            frame.pack(pady=2)
            frame.pack_propagate(False)
            frame.configure(height=620, width=620, bg='#59bfff')
            window_3.mainloop()
    artist = entry_1.get()
    window.destroy()
    window_2 = tkn.Tk()
    window_2.geometry("500x500")
    window_2.resizable(width=False, height=False)
    frame = tkn.Frame(master=window_2)
    label_1 = tkn.Label(master=window_2, text="Entered query:", height=1, width=18,anchor='w')
    label_1.place(x=138, y=180)
    artist_display = tkn.Label(master=window_2, text=artist, height=1, width=25,anchor='w')
    artist_display.place(x=138, y=205)
    label_2 = tkn.Label(master=window_2, text="Enter the no. of top songs you want:", height=1, width=30,anchor='w')
    label_2.place(x=138, y=230)
    entry_label_2 = tkn.Entry(master=window_2, width=10)
    entry_label_2.place(x=210, y=255)
    button_2 = tkn.Button(master=window_2, text="Click to see Result", width=15, relief='raised', command=top_songs_window)
    button_2.place(x=185, y=280)
    frame.pack(pady=5)
    frame.pack_propagate(False)
    frame.configure(height=475, width=475, bg='grey')
    window_2.mainloop()
    top_songs_window()

def error_window(to_be_showed):
    window_4 = tkn.Tk()
    window_4.geometry("500x500")
    window_4.resizable(width=False, height=False)
    frame = tkn.Frame(master=window_4)
    label_1 = tkn.Label(master=window_4, text=to_be_showed, height=1, width=35,anchor='w')
    label_1.place(x=125, y=235)
    frame.pack(pady=5)
    frame.pack_propagate(False)
    frame.configure(height=475, width=475, bg='grey')
    window_4.mainloop()

window = tkn.Tk()
window.geometry("500x500")
window.resizable(width=False, height=False)
frame = tkn.Frame(master=window)
label_1 = tkn.Label(master=window, text="Enter your query below:", height=1, width=18,anchor='w')
label_1.place(x=138, y=180)
entry_1 = tkn.Entry(master=window, width=31)
entry_1.place(x=138, y=205)
button_1 = tkn.Button(master=window, text="About", width=10, relief='raised')
button_1.place(x=148, y=230)
button_2 = tkn.Button(master=window, text="Top Songs", width=10, relief='raised', command=how_many_top_songs_window)
button_2.place(x=240, y=230)
frame.pack(pady=5)
frame.pack_propagate(False)
frame.configure(height=475, width=475, bg='grey')
window.mainloop()