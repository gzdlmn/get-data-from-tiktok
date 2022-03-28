from attr import attr
import requests
from bs4 import BeautifulSoup

# Get data from people who have tik tok account in the last two days. The number of views of the videos must be more than 50000.
# Account
#Let's create a file to write datas

file = open("data-from-tiktok.txt", "w")
file.close()

gamers = ["gametimego", "hypergamer3d", "life.timelapse", "bro_game77", "game.master_x1"]


for i in range(0,5):
    url = "https://www.tiktok.com/@" + str(gamers[i])
    payload={}
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    page = response._content

    soup = BeautifulSoup(page, 'html.parser')

    mydivs = soup.select('div.tiktok-yz6ijl-DivWrapper.e1u9v4ua1')   # go url, detail page

    def get_video_upload_info(video_url):
        response_video = requests.request("GET", video_url, headers=headers)
        video_page  = response_video._content
        soup_video = BeautifulSoup(video_page, 'html.parser')
        video_a = soup_video.select_one('a.tiktok-12dba99-StyledAuthorAnchor.e10yw27c1')   # like  hypergamer/Hypergamer 15h ago
        return video_a.contents[-1]         #  like 15h ago

    def parse_view_info(view_string):
        views = ""
        selector = "."
        selector_binary = "K"
        selector_binary_million = "M"
        if selector_binary_million in view_string:
            return 1000000 # if there is a view about M, you can write directly
        if selector in view_string:
            selector_indis = view_string.index(".")
            views = int(view_string[:selector_indis]) * 1000 + int(view_string[selector_indis+1:-1]) * 100
            print(views)
            file = open("data-from-tiktok.txt", "a")
            file.write(str(views)+"\n")
            file.close()
            return views
        else:
            if selector_binary in view_string:
                views = view_string.strip("K")
                views = int(views) * 1000
                print(views)
                file = open("data-from-tiktok.txt", "a")
                file.write(str(views)+"\n")
                file.close()
                return views
            else:
                print(view_string)
                file = open("data-from-tiktok.txt", "a")
                file.write(view_string+"\n")
                file.close()
                return int(view_string)

    for div in mydivs: 
        #if (div.find(class_ == "stylelistrow"):
        #   print div
        a_element = div.select_one('a')
        video_url = a_element['href']
        print(a_element['href'])
        file = open("data-from-tiktok.txt", "a")
        file.write("\n\n"+"Link: "+a_element['href']+"\n")
        file.close()
        video_upload_string = get_video_upload_info(video_url)    # returned 15h
        print(video_upload_string)     # written 15h ago
        file = open("data-from-tiktok.txt", "a")
        file.write(video_upload_string+"\n")
        file.close()

        strong_element = a_element.find("strong", {"data-e2e" : "video-views"})
        view_info = strong_element.contents[0]
        print(view_info)
        file = open("data-from-tiktok.txt", "a")
        file.write(view_info+"\n")
        file.close()

        if(video_upload_string[1] == 'h' or video_upload_string[1] == 'm' or
        video_upload_string[2] == 'm' or video_upload_string[0:2] == '1d' or 
        video_upload_string[0:2] == '2d'):
            if parse_view_info(view_info) > 50000:
                print("This video is uploaded in the last 2 days AND watched more than 50000")
                file = open("data-from-tiktok.txt", "a")
                file.write("********************This video is uploaded in the last 2 days AND watched more than 50000***********************************\n")
                file.close()

        print("--------")