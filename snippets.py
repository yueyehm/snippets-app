import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    # try:
    #     command = "insert into snippets values (%s, %s)"
    #     cursor.execute(command, (name, snippet))
    # except psycopg2.IntegrityError as e:
    #     connection.rollback()
    #     command = "update snippets set message=%s where keyword=%s"
    #     cursor.execute(command, (snippet, name))
    # connection.commit()
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("insert into snippets values (%s, %s)", (name, snippet))
    except psycopg2.IntegrityError as e:
        with connection, connection.cursor() as cursor:
            cursor.execute("update snippets set message=%s where keyword=%s", (name, snippet)) 
    
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name.
   
    If there is no such snippet...

    Returns the snippet.
    """
    logging.info("Get the snippet {!r}".format(name))
    # cursor = connection.cursor()
    # command = "select message from snippets where keyword = %s"
    # cursor.execute(command, (name,))
    # message = cursor.fetchone()
    # connection.commit()
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        message = cursor.fetchone()
    
    if message:
        return message
    else:
        return "No such snippets"

    return ""    
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    # Subparse for the get command
    logging.debug("Constructing get subparser") 
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    

    arguments = parser.parse_args(sys.argv[1:])
     # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    