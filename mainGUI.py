import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from scraper_db import scrape_and_save_all_posts, delete_all_posts
from scraper_json_runner import convert_json_to_speech, convert_to_json

# Switching functions
def switch_to_delete():
    stacked_widget.setCurrentIndex(4)

def switch_to_TTS():
    stacked_widget.setCurrentIndex(3)

def switch_to_json():
    stacked_widget.setCurrentIndex(2)

def switch_to_scraper():
    stacked_widget.setCurrentIndex(1)

def switch_to_selection():
    stacked_widget.setCurrentIndex(0)

def create_button_layout(buttons):
    button_layout = QHBoxLayout()
    for button in buttons:
        button_layout.addWidget(button)
    button_layout.setAlignment(Qt.AlignCenter)
    return button_layout

def scrape_subreddit():
    scrape_and_save_all_posts(subreddit.text())


# Create the application
scraperGUI = QApplication(sys.argv)

window = QWidget()
stacked_widget = QStackedWidget()
window.setWindowTitle("Main Selection")
window.resize(500, 300)

# Main buttons
scrapeButton = QPushButton("Scrape Reddit Posts")
convertToJsonButton = QPushButton("Convert to JSON")
converToTTSButton = QPushButton("Convert Text-To-Speech")
deletePostsButton = QPushButton("Delete Posts")

# Selection Layout (index 0)
selectionLayout = QVBoxLayout()
selectionLayout.addWidget(scrapeButton)
selectionLayout.addWidget(convertToJsonButton)
selectionLayout.addWidget(converToTTSButton)
selectionLayout.addWidget(deletePostsButton)
selectionWidget = QWidget()
selectionWidget.setLayout(selectionLayout)

# Scraper Layout (index 1)
scrapeLayout = QVBoxLayout()

# Add a spacer at the top to push everything down
scrapeLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Spacer at top

subreddit = QLineEdit()
subreddit.setPlaceholderText("Enter subreddit name")

scrapeBegin = QPushButton("Begin")
scrapeBegin.clicked.connect(scrape_subreddit)
back = QPushButton("Back")
back.clicked.connect(switch_to_selection)

# Spacer item between textbox and buttons
scrapeLayout.addWidget(subreddit)
scrapeLayout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Add a small spacer

scrapeButtonLayout = create_button_layout([scrapeBegin, back])
scrapeLayout.addLayout(scrapeButtonLayout)

scrapeWidget = QWidget()
scrapeWidget.setLayout(scrapeLayout)

# JSON Conversion Layout (index 2)
JsonLayout = QVBoxLayout()

# Add a spacer at the top to push everything down
JsonLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Spacer at top

JsonLabel = QLabel("Converting Scrapped to JSON")
JsonBegin = QPushButton("Begin")
JsonBack = QPushButton("Back")
JsonBack.clicked.connect(switch_to_selection)

JsonButtonLayout = create_button_layout([JsonBegin, JsonBack])

JsonLayout.addWidget(JsonLabel)
JsonLayout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Spacer between label and buttons
JsonLayout.addLayout(JsonButtonLayout)

JsonWidget = QWidget()
JsonWidget.setLayout(JsonLayout)

# Convert to TTS Layout (index 3)
TTSLayout = QVBoxLayout()

# Add a spacer at the top to push everything down
TTSLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Spacer at top

TTSTextBox = QLineEdit()
TTSTextBox.setPlaceholderText("Enter file name")

TTSBegin = QPushButton("Begin")
TTSBack = QPushButton("Back")
TTSBack.clicked.connect(switch_to_selection)

TTSButtonLayout = create_button_layout([TTSBegin, TTSBack])

TTSLayout.addWidget(TTSTextBox)
TTSLayout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Add a small spacer
TTSLayout.addLayout(TTSButtonLayout)

TTSWidget = QWidget()
TTSWidget.setLayout(TTSLayout)

# Delete Posts Layout (index 4)
deleteLayout = QVBoxLayout()

# Set the margin and spacer for proper spacing
deleteLayout.setContentsMargins(20, 20, 20, 20)  # Top, left, bottom, right margins

# Add a spacer at the top to push everything down
deleteLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Spacer at top

deleteLabel = QLabel("Are you sure you want to delete the posts?")
deleteBegin = QPushButton("Begin")
deleteBack = QPushButton("Back")
deleteBack.clicked.connect(switch_to_selection)

deleteButtonLayout = create_button_layout([deleteBegin, deleteBack])

# Add the label and buttons
deleteLayout.addWidget(deleteLabel)
deleteLayout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Add a small spacer
deleteLayout.addLayout(deleteButtonLayout)

deleteWidget = QWidget()
deleteWidget.setLayout(deleteLayout)

# Add widgets to stacked widget
stacked_widget.addWidget(selectionWidget)
stacked_widget.addWidget(scrapeWidget)
stacked_widget.addWidget(JsonWidget)
stacked_widget.addWidget(TTSWidget)
stacked_widget.addWidget(deleteWidget)

# Connect buttons to switch functions
scrapeButton.clicked.connect(switch_to_scraper)
convertToJsonButton.clicked.connect(switch_to_json)
converToTTSButton.clicked.connect(switch_to_TTS)
deletePostsButton.clicked.connect(switch_to_delete)

# Main layout
homeLayout = QVBoxLayout()
homeLayout.addWidget(stacked_widget)
window.setLayout(homeLayout)

window.show()

sys.exit(scraperGUI.exec_())













# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout,QPushButton,QHBoxLayout, QStackedWidget, QLabel

# def switch_to_delete():
#     stacked_widget.setCurrentIndex(4)

# def switch_to_TTS():
#     stacked_widget.setCurrentIndex(3)

# def switch_to_json():
#     stacked_widget.setCurrentIndex(2)

# def switch_to_scraper():
#     stacked_widget.setCurrentIndex(1)

# def switch_to_selection():
#     stacked_widget.setCurrentIndex(0)

# scraperGUI = QApplication(sys.argv)

# window = QWidget()
# stacked_widget = QStackedWidget()
# window.setWindowTitle("Main Selection")
# window.resize(400,200)

# # Main buttons
# scrapeButton = QPushButton("Scrape Reddit Posts")
# convertToJsonButton = QPushButton("Convert to JSON")
# converToTTSButton = QPushButton("Convert Text-To-Speech")
# deletePostsButton = QPushButton("Delete Posts")

# # Layouts

# #selection index 0
# selectionLayout = QVBoxLayout()
# selectionLayout.addWidget(scrapeButton)
# selectionLayout.addWidget(convertToJsonButton)
# selectionLayout.addWidget(converToTTSButton)
# selectionLayout.addWidget(deletePostsButton)
# selectionWidget = QWidget()
# selectionWidget.setLayout(selectionLayout)

# # Scraper layout index 1
# scrapeLayout = QVBoxLayout()
# scrapeButtonLayout = QHBoxLayout()

# subreddit = QLineEdit()
# subreddit.setPlaceholderText("Subreddit")

# scrapeBegin = QPushButton("Begin")
# #add implementationfor begin
# back = QPushButton("Back")
# back.clicked.connect(switch_to_selection)
# scrapeButtonLayout.addWidget(scrapeBegin)
# scrapeButtonLayout.addWidget(back)

# scrapeLayout.addWidget(subreddit)
# scrapeLayout.addLayout(scrapeButtonLayout)
# scrapeWidget = QWidget()
# scrapeWidget.setLayout(scrapeLayout)


# #conver to JSON index 2
# JsonLayout = QVBoxLayout()
# JsonButtonLayout = QHBoxLayout()

# JsonBegin = QPushButton("Begin")
# JsonBack = QPushButton("Back")
# JsonBack.clicked.connect(switch_to_selection)
# JsonButtonLayout.addWidget(JsonBegin)
# JsonButtonLayout.addWidget(JsonBack)

# JsonLabel = QLabel("Converting Scrapped to JSON")
# JsonLayout.addWidget(JsonLabel)
# JsonLayout.addLayout(JsonButtonLayout)

# JsonWidget = QWidget()
# JsonWidget.setLayout(JsonLayout)

# #conver JSON to TTS index 3
# TTSLayout = QVBoxLayout()
# TTSButtonLayout = QHBoxLayout()

# TTSBegin = QPushButton("Begin")
# TTSBack = QPushButton("Back")
# TTSBack.clicked.connect(switch_to_selection)

# TTSButtonLayout.addWidget(TTSBegin)
# TTSButtonLayout.addWidget(TTSBack)

# TTSTextBox = QLineEdit()
# TTSTextBox.setPlaceholderText("Enter JSON name")
# TTSLayout.addWidget(TTSTextBox)
# TTSLayout.addLayout(TTSButtonLayout)

# TTSWidget = QWidget()
# TTSWidget.setLayout(TTSLayout)

# #delete posts index 4
# deleteLayout = QVBoxLayout()
# deleteButtonLayout = QHBoxLayout()

# deleteBegin = QPushButton("Begin")
# deleteBack = QPushButton("Back")
# deleteBack.clicked.connect(switch_to_selection)

# deleteButtonLayout.addWidget(deleteBegin)
# deleteButtonLayout.addWidget(deleteBack)

# deleteLabel = QLabel("Are you sure?")

# deleteLayout.addWidget(deleteLabel)
# deleteLayout.addLayout(deleteButtonLayout)

# deleteWidget = QWidget()
# deleteWidget.setLayout(deleteLayout)



# # Add widgets to stacked widget
# stacked_widget.addWidget(selectionWidget)
# stacked_widget.addWidget(scrapeWidget)
# stacked_widget.addWidget(JsonWidget)
# stacked_widget.addWidget(TTSWidget)
# stacked_widget.addWidget(deleteWidget)

# # Connect the scrape button to the switch function
# scrapeButton.clicked.connect(switch_to_scraper)
# convertToJsonButton.clicked.connect(switch_to_json)
# converToTTSButton.clicked.connect(switch_to_TTS)
# deletePostsButton.clicked.connect(switch_to_delete)

# # Main layout
# homeLayout = QVBoxLayout()
# homeLayout.addWidget(stacked_widget)
# window.setLayout(homeLayout)

# window.show()

# sys.exit(scraperGUI.exec_())