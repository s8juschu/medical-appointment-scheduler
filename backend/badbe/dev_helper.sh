#! /bin/bash


FILE_RESET_SQLITE="./reset_sqlite.sh"
FILE_VENV_ACTIVATE="./venv/bin/activate"
FILE_MOCK_PY="./mocker.py"

check_file_exists() {
  if [ ! -f "$1" ]; then
    echo "[Error: File $1 does not exist"]
  fi
}

activate_venv() {
  if source "$FILE_VENV_ACTIVATE" ; then
    return 0
  else
    echo "[ERROR: Cannot activate venv ("$FILE_VENV_ACTIVATE").]"
    return 1
  fi
}

run_dev_server() {
  check_file_exists "$FILE_VENV_ACTIVATE"
  activate_venv
  echo "[Start dev server]"
  python3 manage.py runserver &
  sleep .5
  deactivate
  echo "[Done]"
}

rebuild_sqlite_db() {
  check_file_exists "$FILE_VENV_ACTIVATE"
  activate_venv
  echo "[Start resetting migrations]"
  echo "[Deleting sqlite database]"
  rm db.sqlite3
  echo "[Deleting all migrations...]"
  find ./polls/migrations -type f -name '0*' -exec echo "    {}" \; -exec rm {} \;
  echo "[Makemigrations]"
  python3 manage.py makemigrations
  echo "[Migrate]"
  python3 manage.py migrate
  deactivate
  echo "[Done]"
}

create_superuser() {
  #
  # Instructs thje backend to create a superuser (admin).
  #
  check_file_exists "$FILE_VENV_ACTIVATE"
  activate_venv
  echo "[Start creating new superuser]"
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(username='admin', email='admin@test.de', first_name='Ad', last_name='Ministrator', password='supersecret')" | python3 manage.py shell
  if [ "$?" -ne 0 ]; then
    echo "[Error: Failed creating a superuser]"
  fi
  deactivate
  echo "[Done]"
}

create_mock_departments() {
  #
  # Runs a the python script which instructs the backend to create some mock departments.
  #
  check_file_exists "$FILE_MOCK_PY"
  echo "[Start creating mock departments]"
  pkill -f runserver
  run_dev_server
  python3 "$FILE_MOCK_PY" mock-departments
  if [ "$?" -ne 0 ]; then
    echo "[Error: Failed to create mock departments]"
    pkill -f runserver
    return 1
  fi
  echo "[Done]"
}

create_mock_employees() {
  #
  # Runs a the python script which instructs the backend to create some mock employees.
  #
  check_file_exists "$FILE_MOCK_PY"
  echo "[Start creating mock employees]"
  pkill -f runserver
  run_dev_server
  python3 "$FILE_MOCK_PY" mock-employees
  if [ "$?" -ne 0 ]; then
    echo "[Error: Failed to create mock employees]"
    pkill -f runserver
    return 1
  fi
  echo "[Done]"
}


try() {
  #
  # A little try-except-finally wrapper.
  #
  "$1"
  RETURN_CODE="$?"
  EXECUTE_ON_ERROR="$2"
  if [ $RETURN_CODE -ne 0 ]; then
    echo "[ERROR]"
    if [ "$EXECUTE_ON_ERROR" != "" ]; then
      "$EXECUTE_ON_ERROR"
    fi
    exit 1
  fi
}


show_help() {
  #
  # Shows the usage page for this script.
  #
  echo ""
  echo "Usage:"
  echo "    $(basename $0) - automating recurring dev management workflows"
  echo ""
  echo "    $(basename $0) <option1> [<option2> ...]"
  echo ""
  echo "options:"
  echo "    new-sqlite          Runs Django commands to re-build the sqlite database. This deletes the current sqlite and migration files."
  echo "    new-superuser       Runs Django commands to create a new superuser 'admin' (email: 'admin@test.de', password: 'supersecret')."
  echo "    mock-departments    Create some mock departments in the backend. (See the python mock script.)"
  echo "    mock-employees      Create some mock employees in the backend. (See the python mock script.)"
  echo "    help                Shows this help page."
}


main() {
  #
  # Parses the command line options and initiates all the requested jobs.
  #

  PARAMS=""
  if [ "$#" -eq 0 ]; then
    show_help
  fi

  while (( "$#" )); do
    case "$1" in
      runserver)
        try run_dev_server
        shift
        ;;
      new-sqlite)
        try rebuild_sqlite_db
        shift
        ;;
      new-superuser)
        try create_superuser
        shift
        ;;
      mock-departments)
        try create_mock_departments
        shift
        ;;
      mock-employees)
        try create_mock_employees
        shift
        ;;
      help|-h|--help)
      show_help
      shift
      ;;
      --) # end argument parsing
        shift
        break
        ;;
      *) # unsupported argument
        echo "[Error: Unsupported option '$1']" >&2
        exit 1
        ;;
    esac
  done
}

main "$@"
