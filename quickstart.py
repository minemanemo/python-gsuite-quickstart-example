from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.orgunit',
    'https://www.googleapis.com/auth/admin.directory.group'
    ]

# TODO:
# - my_customer 이 무엇인지
# - 재로그인 없이 refresh token 발급이 가능한지.

def main():
    creds = None

    # 토큰 존재 시 사용하도록 한다.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            print(dir(token))
            creds = pickle.load(token)

    print(dir(creds))
    print(creds.valid)
    print(creds.expired)
    print(creds.refresh_token)
    # 로그인 과정, 갱신 필요시 갱신, 로그인 필요 시 재로그인.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('check')
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    # Users
    results = service.users().list(customer='C00gjxxvi', orderBy='email').execute()
    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            print(u'- {0}'.format(user['name']['fullName']))
            print(u' * 소속 : {0}'.format(user['orgUnitPath']))
            print(u' * E-mail : {0}'.format(user['primaryEmail']))
            # print(u' * Phone : {0}'.format(user['phones'][0]['value']))
            res = service.users().get(userKey="minhoe@netman.page", projection="full").execute()
            pass
        

    print()

    # Oraniztion
    result2 = service.orgunits().list(customerId='C00gjxxvi', type='all').execute()
    organ = result2.get('organizationUnits', [])

    if not organ:
        print('No organ in the domain.')
    else:
        print('Organ:')
        for org in organ:
            print(u'{0} ({1})'.format(org['name'], org['orgUnitPath']))
    print()

    # Groups
    result3 = service.groups().list(domain='netman.page').execute()
    groups = result3.get('groups', [])

    if not groups:
        print('No groups in the domain.')
    else:
        print('Groups:')
        for group in groups:
            print(u'{0} ({1})'.format(group['name'], group['email']))

if __name__ == '__main__':
    main()
# [END admin_sdk_directory_quickstart]
