from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os
from dotenv import load_dotenv
import logging

class InstaWrapper:

    def __init__(self) -> None:
        load_dotenv('./hfm.env')
        self.user = os.getenv('INSTA_USER')
        self.password = os.getenv('INSTA_PW')
        self.cl = Client()
        self.cl.delay_range = [1, 3]
        self.__login_user()


    def __login_user(self):
        """
        Attempts to login to Instagram using either the provided session information
        or the provided username and password.
        """
        session = None

        if os.path.exists("instagrapi-session.json"):
            session = self.cl.load_settings("instagrapi-session.json") # returns None otherwise

        login_via_session = False
        login_via_pw = False

        if session:
            try:
                self.cl.set_settings(session)
                self.cl.login(self.user, self.password)

                # check if session is valid
                try:
                    self.cl.get_timeline_feed()
                except LoginRequired:
                    logging.info("Session is invalid, need to login via username and password")

                    old_session = self.cl.get_settings()

                    # use the same device uuids across logins
                    self.cl.set_settings({})
                    self.cl.set_uuids(old_session["uuids"])

                    self.cl.login(self.user, self.password)
                login_via_session = True
            except Exception as e:
                logging.info("Couldn't login user using session information: %s" % e)

        if not login_via_session:
            try:
                logging.info("Attempting to login via username and password. username: %s" % self.user)
                if self.cl.login(self.user, self.password):
                    login_via_pw = True
                    self.cl.dump_settings("instagrapi-session.json")
            except Exception as e:
                logging.info("Couldn't login user using username and password: %s" % e)

        if not login_via_pw and not login_via_session:
            raise Exception("Couldn't login user with either password or session")
    
    def upload_photo(self, image_url, image_caption):
        self.cl.photo_upload(image_url, image_caption)

class InstaWrapperMock:
    def __init__(self) -> None:
        pass

    def upload_photo(self, image_url, image_caption):
        pass


#insta = InstaWrapper()
#insta.upload_photo('./cake.jpg', 'a hfm with cake \n\n#happy #test')
