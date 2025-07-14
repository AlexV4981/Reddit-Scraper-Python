import scrape
import scrape_db
import scrape_json_runner

cont = "y"
while cont == "y":
    print("Menu\n1) Scrape posts\n2)Convert to JSON\n3)Convert JSON to TTS\n4)Do all\n5)Wipe")
    choice = input("Option(1-5): ")
    if choice == '1':
        subreddit = input(str("Enter subreddit: "))
        scrape_db.scrape_and_save(subreddit)
    elif choice == '2':
        scrape_json_runner.convert_to_json()
    elif choice == '3':
        scrape_json_runner.convert_json_to_speech()
    elif choice == '4':
        subreddit = input(str("Enter subreddit: "))
        scrape_db.scrape_and_save(subreddit)
        print("Converting to JSON")
        scrape_json_runner.convert_to_json()
        scrape_json_runner.convert_json_to_speech()
        print(f"Successfully completed run for: {subreddit}")
    elif choice == '5':
        scrape_db.delete_all_posts()
    
    
    cont = input(str("Continue? y/n: ")) 
