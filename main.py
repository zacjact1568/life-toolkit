def menu() -> bool:
    option = input(
        'Select one option to continue:\n'
        '[A] Blog post image name rectifier\n'
        '[*] Exit\n'
    )
    if option == 'A':
        from blog import post_image_name_rectifier
        return post_image_name_rectifier()
    elif option == '*':
        return True
    else:
        print(f'No option match: {option}')
        return False


if __name__ == '__main__':
    done = menu()
    while not done:
        done = menu()
    print('Bye')
