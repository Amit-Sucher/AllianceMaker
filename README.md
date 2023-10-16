Meet  **AllianceMaker**

AllianceMaker is a Python application that automates the process of selecting and forming 'alliances' for robotics competitions based on various team metrics.
It ranks teams according to certain defined criteria such as their autonomous score, tele-operation score as well as a bonus score.
The application then simulates the alliance selection process and generates alliances according to this logic.
Each alliance is constituted by a team leader (highest-ranking teams) and other lower-ranking teams. 

Features
- Importing team data from a CSV file
- Calculating scores for each team based on several categories.
- Ranking teams based on their total scores.
- Forming alliances by simulating the competition's alliance selection process.
- Printing the alliances in the console.

Key Concepts Used
- Dictionary in Python: This program uses Python dictionaries to store the team data imported from the CSV file.
- File I/O: The program reads data from a CSV file.
- Sorting and Lambda functions: Sorting operation is performed on the data to rank the teams and for alliance formation.
- List and Dictionary comprehensions: Used extensively for manipulating lists and dictionaries.

### Importing Data 

The program begins by importing team data from a CSV file using the Python's built-in csv module. The imported data is stored in a Python dictionary.

### Calculating Scores 

Once the data is imported, the program calculates scores for each team based on several categories. The scores are calculated using predefined rules. If a team excels in a category, it gets a high score, and vice versa.

### Ranking Teams

After calculating the scores, the program ranks the team based on their total scores. The total score of a team is the sum of the scores in each category plus any bonus points earned.

### Forming Alliances 

The alliance formation process is the main selling point of this program. The program simulates the alliance formation process which happens at the competition. The alliance formation process is divided into two rounds — first round and second round:

- In the first round, top 8 teams are selected as alliance leaders. They are then allowed to select a partner from the remaining lower-ranked teams.
- In the second round, the alliance leaders choose again in reverse order.


### Printing Alliances

The program then prints the alliances in the console. The alliances are displayed in a user-friendly format. For each alliance, the program prints the team number of the alliance leader and the team number of chosen partner.


### Details 
If you have any questions about the program, you are more than welcome to send me a message on discord! (discord username: amit6738)

