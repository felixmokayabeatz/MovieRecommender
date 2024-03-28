import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from recommendation import MovieRecommendationEngine
from theme import create_theme_selector
import theme
import recommendation


class MovieRecommendationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting up window properties
        self.setWindowTitle("Movie Recommendation App")
        self.setGeometry(100, 100, 600, 400)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout(central_widget)

        # Title label
        font = QFont()
        font.setBold(True)
        label = QLabel("Enter Movie Preferences", self)
        label.setFont(font)
        layout.addWidget(label)

        # User input fields
        self.rating_input = QLineEdit(self)
        self.rating_input.setFont(font)
        self.rating_input.setPlaceholderText("Enter Rating")
        layout.addWidget(self.rating_input)

        self.votes_input = QLineEdit(self)
        self.votes_input.setFont(font)
        self.votes_input.setPlaceholderText("Enter Votes")
        layout.addWidget(self.votes_input)

        self.year_input = QLineEdit(self)
        self.year_input.setFont(font)
        self.year_input.setPlaceholderText("Enter Year")
        layout.addWidget(self.year_input)

        # Recommendation label
        self.recommendation_label = QLabel(self)
        layout.addWidget(self.recommendation_label)

        # Blinking effect setup with QTimer and QMovie
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_text_color)
        self.blink_counter = 0

        self.theme_group = create_theme_selector(self)
        layout.addWidget(self.theme_group)


        # Get recommendations button
        self.button = QPushButton("Get Recommendations", self)
        self.button.clicked.connect(self.show_recommendations)
        layout.addWidget(self.button)

        # Get the directory where the executable is located
        self.exe_dir = os.path.dirname(sys.argv[0])

        # Load the recommendation engine using the dynamically obtained file path
        data_file_path = os.path.join(self.exe_dir, 'data', 'IMDB-Movie-Data.csv')
        self.recommendation_engine = MovieRecommendationEngine(data_file_path)

    def show_recommendations(self):
        # Get user input
        rating_text = self.rating_input.text()
        votes_text = self.votes_input.text()
        year_text = self.year_input.text()

        if not (rating_text or votes_text or year_text):
            # Display error message with movie
            self.recommendation_label.clear()          
            self.recommendation_label.setStyleSheet("color: red; font-weight: bold;")
            self.recommendation_label.setText("Please fill in at least one field.")
            return

    

        try:
            # Convert input values to floats, handling empty fields with default values
            user_rating = float(rating_text) if rating_text else 0.0
            user_votes = float(votes_text) if votes_text else 0.0
            user_year = float(year_text) if year_text else 0.0

            # Use the recommendation engine to get recommendations
            recommended_movies = self.recommendation_engine.get_recommendations(user_rating, user_votes, user_year)

            # Display recommendations in the label
            self.recommendation_label.clear()
            self.recommendation_label.setText(f"<font color = 'black'><b>Recommended Movies:</b><br>")

            # Display up to 5 recommended movies
            for _, movie in recommended_movies.iterrows():
                self.recommendation_label.setText(
                    f"{self.recommendation_label.text()}<br>"
                    f"<font color='black'><b>Title: {movie['Title']}</b></font><br>"
                    f"<font color='black'><b>Rating: {movie['Rating']}</b></font><br>"
                    f"<font color='black'><b>Year: {int(movie['Year'])}</b></font><br>"
                    f"<font color='black'><b>Description:</b></font><br><font color='black'>{self.format_description(movie['Description'])}</font><br>"
                    f"<font color='black'><b>=============================</b></font><br>"
                )

        except ValueError:
            # Display error message if conversion from string to float fails
            self.recommendation_label.clear()
            self.recommendation_label.setStyleSheet("color: red; font-weight: bold;")
            self.recommendation_label.setText("Please enter valid numbers.")

            self.blink_timer.start(10)


    def format_description(self, description):
        # Replace line breaks with <br> tags
        formatted_description = description.replace('\n', '<br>')

        # Split the description into words
        words = formatted_description.split()

        # Add a new line after every 20 words
        words_per_line = 20
        formatted_lines = [words[i:i+words_per_line] for i in range(0, len(words), words_per_line)]
        formatted_description = '<br>'.join([' '.join(line) for line in formatted_lines])

           # Make the description italic using <i> tags
        formatted_description = f'<b>{formatted_description}</b>'

        return formatted_description


    def toggle_text_color(self):
        self.blink_counter += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MovieRecommendationApp()
    window.show()
    sys.exit(app.exec_())
