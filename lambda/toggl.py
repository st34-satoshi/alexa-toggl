# coding: utf-8

import requests
from requests.auth import HTTPBasicAuth
import json
import datetime


class TogglDriver:

    def __init__(self, _token):
        self._token = _token  # api_token
        self._workspace_id = self.get_workspace_id(self._token)
        self.projects_dictionary = self.get_projects(_token, self._workspace_id)
        self._headers = {'Content-Type': 'application/json'}

    @staticmethod
    def create_project_and_title(start_name):
        if start_name == "一日":
            return "Life", "morning"
        if start_name == "睡眠":
            return "Sleep", "night"
        if start_name == "読書":
            return "Hobby", "book"
        if start_name == "行ってきます":
            return "Moving", "lab"
        if start_name == "食事":
            return "Life", "Food"
        if start_name == "テレビ":
            return "Play", "TV"
        if start_name == "アットコーダー":
            return "AtCoder", "practice"

    def is_project(self, project_name):
        if project_name in self.projects_dictionary:
            return True
        return False

    @staticmethod
    def get_workspace_id(api_token):
        # get workspace id from api/v8/workspaces
        r = requests.get('https://www.toggl.com/api/v8/workspaces',
                         auth=(api_token, 'api_token'))
        if r.status_code != 200:
            print("Error: cannot get workspace id. please check the token.")
            return ""

        # JSON形式でデータのエクスポート
        data = r.json()
        Data = data[0]
        return Data['id']

    @staticmethod
    def get_projects(api_token, work_space_id):
        # return projects dictionary
        p_dictionary = {}
        r = requests.get('https://www.toggl.com/api/v8/workspaces/{0}/projects'.format(work_space_id),
                         auth=(api_token, 'api_token'))
        if r.status_code != 200:
            print("Error: cannot get projects. please check the token.")
            return p_dictionary

        data = r.json()
        for d in data:
            p_dictionary[d["name"]] = d["id"]
        return p_dictionary

    def get_running_time_entry(self):
        # return time entry id of current entry
        r = requests.get('https://www.toggl.com/api/v8/time_entries/current',
                         auth=HTTPBasicAuth(self._token, 'api_token'))
        if r.status_code != 200:
            print("Error: cannot get running time entry. please check the token.")
            return ""
        data = r.json()['data']
        if data is None:
            return None
        return data['id']

    def start(self, description, project):
        if project in self.projects_dictionary:
            pid = self.projects_dictionary[project]
        else:
            # when no project, make it here.
            self.create_project(project)
            pid = self.projects_dictionary[project]

        params = {"time_entry": {"description": description, "pid": pid, "created_with": "python"}}
        r = requests.post('https://www.toggl.com/api/v8/time_entries/start',
                          auth=HTTPBasicAuth(self._token, 'api_token'),
                          headers=self._headers,
                          data=json.dumps(params))
        print('time entry start. HTTP status :', r.status_code)

    def create_project(self, project_name):
        # '{"project":{"name":"An awesome project","wid":777,"template_id":10237,"is_private":true,"cid":123397}}'
        params = {"project":{"name": project_name, "wid": self._workspace_id, "is_private": True}}
        r = requests.post('https://www.toggl.com/api/v8/projects',
                          auth=HTTPBasicAuth(self._token, 'api_token'),
                          headers=self._headers,
                          data=json.dumps(params))
        print('create project. HTTP status :', r.status_code)
        self.projects_dictionary = self.get_projects(self._token, self._workspace_id)

    def stop(self, running_time_entry_id):
        url = 'https://www.toggl.com/api/v8/time_entries/' + str(running_time_entry_id) + '/stop'
        r = requests.put(url, auth=HTTPBasicAuth(self._token, 'api_token'), headers=self._headers)

        print('time entry stop. HTTP status :', r.status_code)
        return r

    def get_reports(self, mail_address, project_list, date):
        # return each project total time
        # ['Life', 'University', 'Moving', 'Hobby', 'Play', 'Communication']
        params = {
            'user_agent': mail_address,
            'workspace_id': self._workspace_id,
            'since': date,
            'until': date,
        }
        r = requests.get('https://toggl.com/reports/api/v2/details',
                         auth=HTTPBasicAuth(self._token, 'api_token'),
                         params=params)
        if r.status_code != 200:
            print("Error: cannot get reports. please check the token and email. mail={0}, token={1}".format(mail_address, self._token))
            return None
        data_list = r.json()['data']
        # make each project dictionary
        each_project_total_time_dictionary = {}  # value: timedelta
        for project in project_list:
            each_project_total_time_dictionary[self.projects_dictionary[project]] = datetime.timedelta()
        for data_dict in data_list:
            if data_dict['pid'] in each_project_total_time_dictionary:
                start_time = data_dict['start'].split('+')[0]
                dt_start = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
                end_time = data_dict['end'].split('+')[0]
                dt_end = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
                each_project_total_time_dictionary[data_dict['pid']] += dt_end - dt_start

        each_project_total_time_list = []
        for project in project_list:
            each_project_total_time_list.append(
                each_project_total_time_dictionary[self.projects_dictionary[project]].seconds // 60)

        return each_project_total_time_list
