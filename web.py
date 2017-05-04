import socketserver
import json
import http.client
import http.server


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"
    OPENFDA_API_SEARCH ="?limit=10&search=patient.drug.medicinalproduct:"
    OPENFDA_API_COMPANY_SEARCH = "?limit=10&search=companynumb:"

    def get_main_page(self):
        html="""
        <html>
            <head>
            </head>
            <body>
                <h1>OpenFDA Client</h1>


                <form method="get"action="listDrugs">
                    <input type= "submit" value ="Drug List: Enviar"></input>
                </form>


                <form method="get" action = "searchDrug">
                    <input type= "submit" value ="Drug Search"></input>
                    <input type= "text" name ="drug"></input>
                </form>


                <form method = "get"action="listCompanies">
                <input type = "submit" value = "Companies List: Enviar"></input>
                </form>


                <form method="get" action = "searchCompany">
                    <input type= "submit" value ="Companies Search"></input>
                    <input type= "text" name ="company"></input>
                </form>


                <form method="get"action="listGender">
                    <input type= "submit" value = "Gender List"></input>
                </form>


            </body>
        </html>
        """
        return html

    def get_events(self):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?limit=10')
        r1 = conn.getresponse()
        respuesta = r1.read()
        datos = respuesta.decode("utf8")
        events = datos
        return events

    def get_event_search(self):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        drug = self.path.split("=")[1]
        conn.request("GET", self.OPENFDA_API_EVENT + self.OPENFDA_API_SEARCH + drug)
        r1 = conn.getresponse()
        respuesta = r1.read()
        datos = respuesta.decode("utf8")
        events_search = datos
        return events_search

    def get_event_search_companies(self):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        company = self.path.split("=")[1]
        conn.request("GET", self.OPENFDA_API_EVENT + self.OPENFDA_API_COMPANY_SEARCH + company)
        r1 = conn.getresponse()
        respuesta= r1.read()
        datos = respuesta.decode("utf8")
        events_search_companies = datos
        return events_search_companies

    def get_drugs_from_events(self,events):
        drugs=[]
        events_html=""
        for event in events:
            drug = (event['patient']['drug'][0]['medicinalproduct'])
            drugs += [drug]
            events_html += ",".join(drugs)
        return drugs

    def get_companies_from_events(self,events):
        companies=[]
        for event in events:
            companies += [event["companynumb"]]
        return companies

    def get_second_page(self,drugs):

        list_html= """
        <html>
            <head></head>
            <body>
                <ol>
        """
        for i in drugs:
            list_html +="<li>" +i+ "</li>"
        list_html += """

                </ol>
            </body>
        </html>
        """
        return list_html

    def get_gender(self,events):
        genders = []
        for event in events:
            genders += [event['patient']['patientsex'][0]]
        return genders

    def do_GET(self):

        medicamentos= self.get_events()
        main_page = False
        is_event = False
        is_searchDrug =False
        is_companies = False
        is_searchCompany = False
        is_gender = False

        if self.path =="/":
            main_page = True

        elif "/listDrugs" in self.path:
            is_event = True

        elif "searchDrug" in self.path:
            is_searchDrug = True

        elif "/listCompanies" in self.path:
            is_companies = True

        elif "searchCompany" in self.path:
            is_searchCompany = True

        elif "/listGender" in self.path:
            is_gender = True

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        html= self.get_main_page()


        if main_page:
            self.wfile.write(bytes(html, "utf8"))

        elif is_event:
            events_str= self.get_events()
            events=json.loads(events_str)
            events=events['results']
            drugs= self.get_drugs_from_events(events)
            self.wfile.write(bytes(self.get_second_page(drugs), "utf8"))

        elif is_searchDrug:
            events_search = self.get_event_search()
            events_search = json.loads(events_search)
            eventsDrugs = events_search['results']
            companies = self.get_companies_from_events(eventsDrugs)
            html2 = self.get_second_page(companies)
            self.wfile.write(bytes(html2,"utf8"))

        elif is_companies:
            events_str_comp = self.get_events()
            events_comp = json.loads(events_str_comp)
            events_comp_2=events_comp['results']
            company = self.get_companies_from_events(events_comp_2)
            self.wfile.write(bytes(self.get_second_page(company), "utf8"))

        elif is_searchCompany:
            events_search_comp = self.get_event_search_companies()
            events_search = json.loads(events_search_comp)
            eventsCompanies = events_search['results']
            companies_from_drugs = self.get_drugs_from_events(eventsCompanies)
            html2 = self.get_second_page(companies_from_drugs)
            self.wfile.write(bytes(html2,"utf8"))

        elif is_gender:
            events_str_gender = self.get_events()
            events_gender = json.loads(events_str_gender)
            events_gender_2 = events_gender['results']
            gender = self.get_gender(events_gender_2)
            self.wfile.write(bytes(self.get_second_page(gender),"utf8"))
