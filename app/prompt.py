from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from clint.textui import puts, colored, indent, columns

# local imports
import queries

def main():
    """
    User interface/prompting for command line
    """
    col = 90

    # welcome message --------------------------------------------------------------------------------------------------------
    puts(colored.magenta("Welcome to VA Finder!"))
    puts("Find voice actors and the top ten most popular characters they voice for!")
    puts("To get started:")
    with indent(11, quote=colored.magenta("~")):
        puts(columns(["Scroll through menu options using the up and down arrows on your ", col]))
    with indent(11):
        puts(columns(["keyboard, then press Enter to select.", col]))

    with indent(11, quote=colored.magenta("~")):
        puts(columns(["Select \"Help\" for more information and search tips.", col]))

    with indent(11, quote=colored.magenta("~")):
        puts(columns(["Selecting \"Exit\" will close this program.", col]))
    
    with indent(11, quote=colored.magenta("~")):
        with indent(1, quote=colored.green("(New!) ")):
            puts(columns(["Just feel like browsing? Need a low stakes gacha fix?", col]))
        with indent(7, quote=colored.green(">>>>")):
            puts(columns(["The \"Random Character VA!\" option chooses a random popular character to search for!", col]))

    # main menu ---------------------------------------------------------------------------------------------------------------
    while True:
        home = inquirer.select(
            message="Select an Option:", 
            choices=[
                Choice("char", name="Search by Character"),
                Choice("va", name="Search by Voice Actor"),
                Choice("rand_char", name="Random Character VA!"),
                Choice("help", name="Help"),
                Choice(value=None, name="Exit")
            ],
            default=None,
            ).execute()
        
        # search by char selected ----------------------------------------------------------------------------------------------
        if home == "char":
            char_search = inquirer.text(
                message="Enter character name: "
            ).execute()
            print(f"The character you searched was: {char_search}")
                  
            # pass user search terms to query; char results = [(id, (name, anime))]
            char_results = queries.get_char_by_search(char_search)

            # Error
            if len(char_results) == 0:
                puts(colored.red("No results found. Please check your search terms."))
                puts(colored.red("Select \"Help\" for more information."))
                continue
            
            # filter out id; char_list = ['name (anime)',...]
            char_list = [f"{char['char_name']} ({char['anime']})" for char in char_results]
            max_len = 4 if len(char_list) > 4 else len(char_list)
            char_list = char_list[:max_len + 1]
            char_list.append("Return to Main Menu")

            # select from query (tbd)
            char_select = inquirer.rawlist(
                message="Please select the correct character or return to the main menu:",
                choices=char_list,     # choices will use a list passed from query
                default=1,
            ).execute()
            
            # return to main menu
            if char_select == 'Return to Main Menu':
                continue

            # character chosen **get voice actor and va search results from query - pass char_select
            selected_char_id = None
            for char in char_results:
                comparison_str = f"{char['char_name']} ({char['anime']})"
                if comparison_str == char_select:
                    selected_char_id = char['char_id']
                    break
            
            char_and_va_info = queries.get_char_by_id(selected_char_id)
            voiced_chars = queries.get_va_chars(char_and_va_info['va_id'])

            puts(colored.magenta(f"{char_and_va_info['char_name']}"), newline=False)
            print(" is voiced by ", end="")
            puts(colored.green(f"{char_and_va_info['va_name']}.\n"))
            puts(colored.green(f"Top ten characters voiced by {char_and_va_info['va_name']}:\n"))
            puts(colored.cyan(voiced_chars))
            continue
        
        # search by va -------------------------------------------------------------------------------------------------------
        if home == "va":
            va_search = inquirer.text(
                message="Enter voice actor name: "
            ).execute()
            print("The voice actor you searched for was: ", end="")
            puts(colored.green(va_search)) 
            filtered_search = queries.get_va_by_search(va_search)

            # Error
            if len(filtered_search) == 0:
                puts(colored.red("No results found. Please check your search terms."))
                puts(colored.red("Select \"Help\" for more information."))
                continue
            
            va_list = [va['name']['full'] for va in filtered_search]
            max_len = 4 if len(va_list) > 4 else len(va_list)
            va_list = va_list[:max_len + 1]
            va_list.append("Return to Main Menu")

            # select from query
            va_select = inquirer.rawlist(
                message="Please select the correct voice actor, or return to the main menu:",
                choices=va_list,       # list passed from query
                default=1,
            ).execute()
            
            # return to main menu
            if va_select == 'Return to Main Menu':
                continue

            # va chosen (get character search results from query)
            for va in filtered_search:
                if va['name']['full'] == va_select:
                    va_id = va['id']
            voiced_chars = queries.get_va_chars(va_id)
            puts(colored.green(f"Top ten characters voiced by {va_select}:\n"))
            puts(colored.cyan(voiced_chars))
        
        # random character ----------------------------------------------------------------------------------------------------
        if home == "rand_char":

            # call microservice to get random id
            surprise = queries.get_rand_char()
            
            # Microservice error (get_rand_char() returns error string if exeception occurs)
            if type(surprise) is str:
                puts(colored.red(surprise))
                continue
            
            char_and_va_info = queries.get_char_by_id(surprise)

            # Error
            if len(char_and_va_info) == 0:
                puts(colored.red("No results found, sorry about that! Please try again to generate a different random ID."))
                puts(colored.red("Select \"Help\" for more information."))
                continue

            voiced_chars = queries.get_va_chars(char_and_va_info['va_id'])
            print(f"\nYour surprise character is: ", end="")
            puts(colored.magenta(f"{char_and_va_info['char_name']} "), newline=False)
            print(f"from {char_and_va_info['anime']}!")
            puts(colored.magenta(f"{char_and_va_info['char_name']}"), newline=False)
            print(" is voiced by ", end="")
            puts(colored.green(f"{char_and_va_info['va_name']}.\n"))
            puts(colored.green(f"Top ten characters voiced by {char_and_va_info['va_name']}:\n"))
            puts(colored.cyan(voiced_chars))
            continue

        # help/additional info ------------------------------------------------------------------------------------------------
        if home == "help":
            
            puts(colored.green("Sure! Here are some tips for using VA Finder:"))

            with indent(7, quote=colored.green('-->')):
                puts(columns(["Selecting \"Search by Character\" will first search for anime characters ", col]))
            with indent(7):
                puts(columns(["matching your name search. Many characters have similar or the same names, so you will then be able to select from a list of matches. "
                            "Once the character that you're searching for is confirmed, the voice actor who voices that character will "
                            "be displayed, along with the top ten most popular characters they voice for.", col]))

            with indent(7, quote=colored.green('-->')):
                puts(columns(["If you know the voice actor's name already, you can select the ", col]))
            with indent(7):
                puts(columns(["\"Search by voice actor\" option. " 
                            "This option will also display the top five matches from anilist for you to scroll through using the arrows on your keyboard.", col]))
                
            with indent(7, quote=colored.green('-->')):
                puts(columns(["Using both first and last name in either search option increases your", col]))
            with indent(7):
                puts(columns(["chances of finding a match.", col]))

            with indent(7, quote=colored.green('-->')):
                puts(columns(["This tool was built using the anilist API, so the popularity of", col]))
            with indent(7):
                puts(columns(["characters is based on current anilist rankings.", col]))

            with indent(7, quote=colored.green('-->')):
                puts(columns(["Selecting \"Exit\" stops the program.", col]))

        # exit
        if home == None:
            break



if __name__ == "__main__":
    main()