import random

MOCK_QUESTIONS = {
    "Easy": [
        {
            "question": "What is the primary purpose of a database management system?",
            "topic": "Database Fundamentals",
            "points": 5,
        },
        {"question": "Define what a variable is in programming.", "topic": "Programming Basics", "points": 5},
        {"question": "What does CPU stand for?", "topic": "Computer Hardware", "points": 5},
        {
            "question": "What is the difference between hardware and software?",
            "topic": "Computer Fundamentals",
            "points": 5,
        },
        {"question": "What is an operating system?", "topic": "System Software", "points": 5},
    ],
    "Medium": [
        {
            "question": "Explain the concept of object-oriented programming and its main principles.",
            "topic": "Software Engineering",
            "points": 10,
        },
        {
            "question": "What is the difference between a stack and a queue data structure?",
            "topic": "Data Structures",
            "points": 10,
        },
        {
            "question": "Describe the ACID properties in database transactions.",
            "topic": "Database Systems",
            "points": 10,
        },
        {
            "question": "What is machine learning and how does it differ from traditional programming?",
            "topic": "Artificial Intelligence",
            "points": 10,
        },
        {"question": "Explain the concept of recursion with an example.", "topic": "Algorithms", "points": 10},
    ],
    "Hard": [
        {
            "question": "Discuss the trade-offs between different sorting algorithms and when to use each.",
            "topic": "Advanced Algorithms",
            "points": 15,
        },
        {
            "question": "Explain the CAP theorem and its implications for distributed systems.",
            "topic": "Distributed Systems",
            "points": 15,
        },
        {
            "question": "Describe the backpropagation algorithm in neural networks.",
            "topic": "Deep Learning",
            "points": 15,
        },
        {
            "question": "What are design patterns? Explain the Singleton and Observer patterns.",
            "topic": "Software Architecture",
            "points": 15,
        },
        {
            "question": "Discuss the differences between NoSQL and SQL databases with examples.",
            "topic": "Database Architecture",
            "points": 15,
        },
    ],
}


def evaluate_answer(question, answer, difficulty):
    """Mock evaluation - in real implementation, this would use LLM"""
    if len(answer.strip()) < 20:
        return {"score": random.randint(1, 3), "feedback": "Answer too brief. More detail needed.", "points_earned": 1}
    elif len(answer.strip()) < 100:
        return {
            "score": random.randint(3, 7),
            "feedback": "Good attempt, but could be more comprehensive.",
            "points_earned": random.randint(3, 7),
        }
    else:
        return {
            "score": random.randint(7, 10),
            "feedback": "Excellent detailed answer!",
            "points_earned": random.randint(7, 10),
        }
