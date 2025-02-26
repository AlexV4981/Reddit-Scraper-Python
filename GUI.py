import sys,time
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from scraper_db import scrape_and_save_all_posts, delete_all_posts
from scraper_json_runner import convert_json_to_speech, convert_to_json

class ScraperThread(QThread):
    """Worker thread for scraping subreddit posts."""
    scraping_done = pyqtSignal()  # Signal to indicate that scraping is done.
    error_occurred = pyqtSignal(str)  # Signal to report any errors.

    def __init__(self, subreddit_name):
        super().__init__()
        self.subreddit_name = subreddit_name

    def run(self):
        try:
            # Call your scraping function (scrape_and_save_all_posts)
            scrape_and_save_all_posts(self.subreddit_name)
            self.scraping_done.emit()  # Notify that scraping is done
        except Exception as e:
            self.error_occurred.emit(str(e))  # Notify that an error occurred


class SelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reddit Scraper")
        self.resize(500,300)
        # Create the stacked widget for different screens
        self.stacked_widget = QStackedWidget(self)

        # Initialize and add different windows to the stacked widget
        self.create_selection_window()
        self.create_scraper_window()
        #self.create_json_converter_window()
        self.create_TTS_window()

        self.stacked_widget.setCurrentIndex(0)

        # Layout setup
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def create_selection_window(self):
        """Creates the initial selection window layout."""
        selection_layout = QVBoxLayout()

        scrape_button = QPushButton("Scrape Reddit Posts")
        convert_button = QPushButton("Convert to JSON")
        tts_button = QPushButton("Convert to TTS")
        delete_button = QPushButton("Delete Posts")

        # Connect buttons to their respective methods
        scrape_button.clicked.connect(self.switch_to_scraper)
        convert_button.clicked.connect(self.switch_to_json)
        tts_button.clicked.connect(self.switch_to_tts)
        delete_button.clicked.connect(self.switch_to_delete)

        selection_layout.addWidget(scrape_button)
        selection_layout.addWidget(convert_button)
        selection_layout.addWidget(tts_button)
        selection_layout.addWidget(delete_button)

        selection_widget = QWidget()
        selection_widget.setLayout(selection_layout)

        self.stacked_widget.addWidget(selection_widget)

    def create_scraper_window(self):
        """Creates the window for subreddit scraping."""
        scraper_layout = QVBoxLayout()
        scraper_button_layout = QHBoxLayout()

        self.subreddit_input = QLineEdit()
        self.subreddit_input.setPlaceholderText("Enter subreddit name")

        scrape_begin_button = QPushButton("Begin Scraping")
        back_button = QPushButton("Back")
        scrape_begin_button.clicked.connect(self.scrape_subreddit)
        back_button.clicked.connect(self.switch_to_selection)

        scraper_button_layout.addWidget(scrape_begin_button)
        scraper_button_layout.addWidget(back_button)

        scraper_layout.addWidget(self.subreddit_input)
        scraper_layout.addLayout(scraper_button_layout)

        scraper_widget = QWidget()
        scraper_widget.setLayout(scraper_layout)

        self.stacked_widget.addWidget(scraper_widget)
    
    #Button Functions

    #Not needed make the selection button do that and clear the DB
    # def create_json_converter_window(self):
    #     json_layout = QVBoxLayout()
    #     json_button_layout = QHBoxLayout()

    #     self.json_input = QLineEdit()
    #     self.json_input.setPlaceholderText("Json Name")

    #     json_begin_button = QPushButton("Begin Conversion")
    #     back_button = QPushButton("Back")


    #     json_begin_button.clicked.connect(convert_to_json)
    #     back_button.clicked.connect(self.switch_to_selection)

    #     json_button_layout.addWidget(json_begin_button)
    #     json_button_layout.addWidget(back_button)

    #     json_layout.addWidget(self.json_input)
    #     json_layout.addLayout(json_button_layout)

    #     json_widget = QWidget()
    #     json_widget.setLayout(json_layout)

    #     self.stacked_widget.addWidget(json_widget)

    def create_TTS_window(self):
        TTS_layout = QVBoxLayout()
        TTS_Button_Layout = QHBoxLayout()

        self.TTS_input = QLineEdit()
        self.TTS_input.setPlaceholderText("Replace with folder view of JSONS")

        TTS_begin_button = QPushButton("Begin Conversion")
        back_button = QPushButton("Back")

        TTS_begin_button.clicked.connect(convert_json_to_speech)
        back_button.clicked.connect(self.switch_to_selection)

        TTS_Button_Layout.addWidget(TTS_begin_button)
        TTS_Button_Layout.addWidget(back_button)

        TTS_layout.addWidget(self.TTS_input)
        TTS_layout.addLayout(TTS_Button_Layout)

        TTS_widget = QWidget()
        TTS_widget.setLayout(TTS_layout)

        self.stacked_widget.addWidget(TTS_widget)

    def create_delete_confirmation_window(self):
        confirmation = QLabel("Are you sure?")
        confirmation_button_layout = QHBoxLayout()
        confirmation_layout = QVBoxLayout()

        confirmation_button = QPushButton("Confirm")
        confirmation_button.clicked.connect(self.delete_posts_db)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.switch_to_selection)

        confirmation_button_layout.addWidget(confirmation_button)
        confirmation_button_layout.addWidget(cancel_button)

        confirmation_layout.addWidget(confirmation)
        confirmation_layout.addLayout(confirmation_button_layout)

        

    def scrape_subreddit(self):
        subreddit_name = self.subreddit_input.text().strip()
        if subreddit_name:
            self.scraper_thread = ScraperThread(subreddit_name)
            self.scraper_thread.scraping_done.connect(self.on_scraping_done)
            self.scraper_thread.error_occurred.connect(self.on_scraping_error)
            self.scraper_thread.start()
        else:
            self.show_error_message("Please enter a subreddit name!")

    def on_scraping_done(self):
        self.show_message("Scraping completed successfully!")
        self.switch_to_selection()  # Go back to the selection window

    def on_scraping_error(self, error_message):
        self.show_error_message(f"Error occurred: {error_message}")
        self.switch_to_selection()  # Go back to the selection window

    def show_message(self, message):
        message_label = QLabel(message)
        self.layout().addWidget(message_label)
        time.sleep(5)
        self.layout().removeWidget(message_label)
    
    def show_error_message(self, error_message):
        error_label = QLabel(f"Error: {error_message}")
        self.layout().addWidget(error_label)

    def start_scraping(self):
        self.scrape_subreddit()

    def delete_posts_db():
        delete_all_posts()

    #Switches
    def switch_to_selection(self):
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_scraper(self):
        self.stacked_widget.setCurrentIndex(1)

    def switch_to_json(self):
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_tts(self):
        self.stacked_widget.setCurrentIndex(2)

    def switch_to_delete(self):
        self.stacked_widget.setCurrentIndex(3)



app = QApplication(sys.argv) 
window = SelectionWindow()
window.show() 
sys.exit(app.exec_()) 