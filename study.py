from ec import ec
import sys
import id


def usage():
    return """
            python study.py headless
            python study.py
            The default identification will be import from id.py.
        """


if __name__ == '__main__':

    ecampus = ec('e-campus')

    address_mode = False

    if len(sys.argv) < 2:
        ecampus.create_browser()
    else:
        if sys.argv[1] == 'headless':
            ecampus.create_headless_browser()
        elif sys.argv[1] == 'address':
            address_mode = True
            ecampus.create_headless_browser()

    ecampus.init_identification(id.username, id.password)

    ecampus.open_main()
    try:
        ecampus.sign_in()
    except:
        print('failed to sign in')
        exit(300)

    if address_mode:
        ecampus.get_addresses()
    else:
        ecampus.start_watch()

