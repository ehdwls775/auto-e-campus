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

    if len(sys.argv) > 1 and sys.argv[1] == 'headless':
        ecampus.create_headless_browser()
    else:
        ecampus.create_browser()

    ecampus.init_identification(id.username, id.password)

    ecampus.open_main()
    try:
        ecampus.sign_in()
    except:
        print('failed to sign in')
        exit(300)

    ecampus.start_watch()

