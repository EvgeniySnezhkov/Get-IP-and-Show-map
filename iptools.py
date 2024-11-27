import re
import requests
import socket
import webbrowser


class IpTools:
    @staticmethod
    def input_address():
        """
        Get IP address from user or return the current public IP address.
        """
        request = input(
            'Input address (decimal and string supported) or press '
            'Enter to get your public IP\n')

        pattern1 = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', request)
        pattern2 = re.match(r'[a-zA-Z]', request)

        def compliance():
            if pattern1:
                return [request]
            elif pattern2:
                try:
                    ip_address = socket.gethostbyname(request)
                    return [ip_address]
                except socket.gaierror:
                    print(f"IP is introduced incorrectly"
                          f" or page and address not responsing for query"
                          f" {request}, \n Will be shown your public IP")
            else:
                print("IP address not entered\n"
                      "Will be shown your public IP")
                return None

        return compliance()

    @staticmethod
    def get_ip():
        """
        Get the current public IP address.
        """
        IP = requests.get('https://api.ipify.org').text
        return IP

    @staticmethod
    def response(IP):
        """
        Send a request to the IP API to get information about the IP address.
        """
        response = requests.get(f"http://ip-api.com/json/{IP}?lang=en")

        if response.status_code == 200:
            return response.json()
        else:
            print("Error occurred while fetching IP information")
            return None

    @staticmethod
    def ip_info():
        """
        Display information about the IP address.
        """
        input_address = IpTools.input_address()
        if input_address is None:
            IP = IpTools.get_ip()
        elif len(input_address) == 1:
            IP = input_address[0]
        else:
            return None

        response = IpTools.response(IP)
        if response is None:
            return None

        if response["status"] == "fail":
            print("Invalid IP address")
            return None

        for key, value in response.items():
            print(f"[{key.title()}]: {value}")

        return response

    @staticmethod
    def map_show():
        """
        Display the location of the IP address on a map.
        """
        result = IpTools.ip_info()
        if result is None:
            return None

        lat = result["lat"]
        lon = result["lon"]

        urlpath = f'https://www.openstreetmap.org/#map=15/{lat}/{lon}'

        open_map = webbrowser.open_new_tab(urlpath)
        return open_map


IpTools.map_show()
