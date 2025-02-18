import json
from datetime import datetime

# Class to handle the mood journal
class MoodJournal:
    def __init__(self, filename="mood_journal.json"):
        self.filename = filename
        self.entries = self.load_entries()
    
    def load_entries(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def save_entries(self):
        with open(self.filename, "w") as file:
            json.dump(self.entries, file, indent=4)
    
    def add_entry(self, date, mood, thoughts):
        self.entries[date] = {"mood": mood, "thoughts": thoughts}
        self.save_entries()
    
    def view_entries(self):
        for date, entry in self.entries.items():
            print(f"Date: {date}")
            print(f"Mood: {entry['mood']}")
            print(f"Thoughts: {entry['thoughts']}")
            print("\n")

# Class to handle the mindfulness tips
class MindfulnessTips:
    def __init__(self):
        self.tips = [
            "Take a deep breath and count to five.",
            "Focus on the sensations in your body.",
            "Notice your surroundings without judgment.",
            "Take a moment to express gratitude.",
            "Practice mindful listening when talking to others."
        ]
    
    def get_daily_tip(self):
        return self.tips[datetime.now().day % len(self.tips)]

# Main function
def main():
    journal = MoodJournal()
    tips = MindfulnessTips()

    while True:
        print("1. Add Mood Entry")
        print("2. View Mood Entries")
        print("3. Get Daily Mindfulness Tip")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            date = datetime.now().strftime("%Y-%m-%d")
            mood = input("How are you feeling today? ")
            thoughts = input("What's on your mind? ")
            journal.add_entry(date, mood, thoughts)
            print("Entry added successfully!")
        elif choice == "2":
            journal.view_entries()
        elif choice == "3":
            print("Today's Mindfulness Tip: ")
            print(tips.get_daily_tip())
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
