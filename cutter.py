import requests
import urllib
import os.path


def get_api():
    api_key_func = str(input('Input your API key from https://cutt.ly/edit\n> '))
    with open('api_key.txt', 'w+') as file:
        file.write(api_key_func)
        file.close()
    return api_key_func


if not os.path.isfile('api_key.txt'):
    api_key = get_api()
else:
    with open('api_key.txt', 'r') as file:
        api_key = file.read()


def what_to_do_choice():
    what_to_do = str(input('You want to:\n'
                           '1. Short link\n'
                           '2. Get stats of shortened link\n'
                           '~> '
                           ))
    return what_to_do


def short_link(*, prefer_name, url, key):
    response = requests.get('https://cutt.ly/api/api.php?key={}&short={}&name={}'.format(key, url, prefer_name))
    status = str(response.json()['url']['status'])
    if status == '1':
        return 'Link has already shortened'
    elif status == '2':
        return 'Looks like not a link! Please, specify a link'
    elif status == '3':
        return 'This name is already taken'
    elif status == '4':
        return 'Invalid API key! Go to Your profile > Account settings > Api key'
    elif status == '5':
        return 'Link has invalid characters'
    elif status == '6':
        return 'Link provided from blocked domain'
    elif status == '7':
        return response.json()
    else:
        raise Exception


def get_shortened_link(*, url, key):
    r = requests.get('http://cutt.ly/api/api.php?key={}&stats={}'.format(key, url))
    return r.json()


user_choice = what_to_do_choice()


def choice_logic(user_choice):
    if user_choice == '1':
        url = urllib.parse.quote(str(input('Enter a url> ')))
        prefer_name = str(input('Enter prefer name ~> '))
        respond_shorted_link = short_link(url=url, prefer_name=prefer_name, key=api_key)
        if type(respond_shorted_link) == dict:
            with open(f'stats of url.txt', 'w+') as file:
                str_result = ('Full link: ' + respond_shorted_link['url']['fullLink'] + '\n' + 'Short Link: ' +
                              respond_shorted_link['url']['shortLink'])

                file.write(str_result)
                file.close()
                print('Shorted link is: ' + respond_shorted_link['url']['shortLink'])
                print('All info was written to stats of url.txt file in program directory! Check it out')
        else:
            print(respond_shorted_link)
    elif user_choice == "2":
        shorted_link_to_get = str(input('Enter shortened link you want statistic to get ~> '))
        res = get_shortened_link(url=shorted_link_to_get, key=api_key)

        with open(f'stats of url.txt', 'w+') as file:
            str_res = ('Clicks: ' + str(res['stats']['clicks']) + '\n' + "Full Link: " + res['stats'][
                'fullLink'] + '\n' +
                       'facebook clicks: ' + str(res['stats']['facebook']) + '\n' + 'Instagram clicks: ' +
                       str(res['stats']['facebook']) + '\n' + "Other Clicks: " + str(res['stats']['rest']))
            print('All info was written to stats of url.txt file in program directory! Check it out.')
            file.write(str_res)
            file.close()
    else:
        print('[!] Please choose correct action from 1 to 2')
        new_choice = what_to_do_choice()
        choice_logic(new_choice)


if __name__ == "__main__":
    choice_logic(user_choice)
