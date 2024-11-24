

class LocalizationConstants:

    # Interface elements:
    ACTION_REQUEST: str = "\tWhat do you want to do? Enter a command: "

    HELLO_MESSAGE: str = """\tWelcome to the library service application. Here are several functions.
    You can add books, delete them, change their status. You can view the full list of all books and
    find all books by title, author, and year of publication. Let's get started:"""

    REPEAT_COMMAND: str = "\n\tCommand not recognized, please try again\n"

    GOODBYE_MESSAGE: str = "\n\tGoodbye, thank you for using the application!\n"

    FUNCTIONAL_DESCRIPTION: str = """\tView the list of all books: /all
    Add a book: /add
    Delete a book: /delete
    Search for a book: /search
    Change the status of a book: /change-status
    Exit the application: /exit"""

    # Viewing the entire library:
    EMPTY_LIBRARY_WARNING: str = "\tThere are no books in the library"

    # Adding a book:
    ADD_BOOK_INFO_MESSAGE: str = "\tTo add a book, sequentially enter the title, author, and year of publication"
    INPUT_TITLE_MESSAGE: str = "\tEnter the title of the book: "
    INPUT_AUTHOR_MESSAGE: str = "\tEnter the author of the book: "
    INPUT_YEAR_MESSAGE: str = "\tEnter the year of publication: "

    ADD_BOOK_SUCCESS: str = "\tBook successfully added!"

    # Searching for books:
    SEARCH_INFO_MESSAGE: str = """\n\tEnter the title of the book, author, or year of publication.
    You can specify multiple values, separating them with `;` for a global search
    For example: Martin; 1980; Chronicles of War; Procopius
    If you want to find books with exactly specified data, for example, books by J. Rowling
    from 1999, combine the search using &&&
    For example: Martin, Procopius, Rowling&&&1999.
    In this case, all books by Martin and Procopius will be found for all time and all books by Rowling for 1999
    """
    INPUT_QUERY_MESSAGE: str = "\tWhat are we searching for: "

    NO_BOOKS_WARNING: str = "\n\tNo books found for your query\n"

    # Deleting books:
    INPUT_DELETE_IDS_MESSAGE: str = "\tEnter the IDs of the books you want to delete. Separate them with commas: "

    DELETE_BOOKS_SUCCESS: str = "\tSuccessfully deleted"

    DELETE_BOOKS_ERROR: str = "\tThere was a problem with deletion"

    # Changing status:
    INPUT_CHANGING_BOOK_ID_MESSAGE: str = "\tEnter the ID of the book whose status you want to change: "
    INPUT_NEW_STATUS_MESSAGE: str = "\tEnter the new status: "

    CHANGING_STATUS_SUCCESS: str = "\tStatus change was successful"
    CHANGING_STATUS_NO_ID_ERROR: str = "\tNo data about the ID. Please contact technical support or try again"

    # Validation errors:
    EXIST_TITLE_WARNING: str = "\tThere are already books with this title, please check if you want to continue"
    EXIST_BOOK_ERROR: str = """\tYou are trying to add a book that already exists in the database """
    NO_DIGIT_IN_YEAR: str = '\tThe "Year" value contains an unknown character that is not a digit'

    NO_BOOKS_WITH_INPUT_ID_ERROR: str = "\tThere are no books in the database with the specified ID: "
    NOT_ALLOWED_STATUS_ERROR: str = "\tThe entered status is not allowed, please try again"

    # ORM errors:
    ADD_BOOK_ERROR: str = "\tAn error occurred while adding the book, please contact technical support."
    TRY_DELETE_NOT_EXIST_ID_ERROR: str = "\tAttempt to delete a non-existent book with ID"
    JUST_ERROR: str = "\tAn error occurred, please contact technical support"
