import requests
from datetime import datetime
class ScoreGet:
    def __init__(self):
        """
        Declaring the endpoints, apikey
        """
        self.url_get_all_matches = "http://cricapi.com/api/matches"
        self.url_get_score="http://cricapi.com/api/cricketScore"
        self.api_key = "WtN3ZjH3bZboKcYJgumLsaBAtrn2"
        self.unique_id = "1216534"  # unique to every match

    def get_unique_id(self):
        """
        Returns Indian cricket teams match id, if the match is Live
        :return:
        """
        uri_params = {"apikey": self.api_key}
        resp = requests.get(self.url_get_all_matches, params=uri_params)
        resp_dict = resp.json()
        uid_found=0
        for i in resp_dict['matches']:
            if (i['team-1'] == "Sunrisers Hyderabad" or i['team-2'] == "Royal Challengers Bangalore") :
                todays_date = datetime.today().strftime('%Y-%m-%d')
                todays_date = "2020-09-21"
                if todays_date == i['date'].split("T")[0]:
                    uid_found=1
                    self.unique_id=i['unique_id']
                    print(self.unique_id)
                    break
        if not uid_found:
            self.unique_id=-1

        send_data=self.get_score(self.unique_id)
        return send_data
    def get_score(self,unique_id):
        data="" #stores the cricket match data
        if unique_id == -1:
            data="No RCB match Today!"
        else:
            uri_params = {"apikey": self.api_key, "unique_id": self.unique_id}
            resp=requests.get(self.url_get_score,params=uri_params)
            data_json=resp.json()
            #print(data_json)
            try:
                data="Score of team is  "+ "\n" + data_json['stat'] +'\n' + data_json['score']
            except KeyError as e:
                data="Oops! please try again!"
        return data



if __name__ == "__main__":
    match_obj=ScoreGet()
    send_message=match_obj.get_unique_id()
    print(send_message)
    from twilio.rest import Client
    account_sid = 'ACc5def102b232ce1b2d6dd05228177075'
    auth_token = '987d1cb437fb645e12ad4d60258721cb'
    client = Client(account_sid, auth_token)
    message = client.messages.create( body=send_message, from_='whatsapp:+14155238886', to='whatsapp:+917904830532' )