# Driving Instructor Booking System

A desktop-based Driving Instructor Booking System built in Python using CustomTkinter for the interface and SQLite for data storage.

I originally developed this project for my A Level Computer Science NEA, where it achieved 68/75 and the highest mark in my cohort. I have since gone back through the project to fix bugs, clean parts of the code up and prepare it for GitHub.

## Features

The system has separate accounts and functionality for students, instructors and administrators.

Main features include:

- Student, instructor and administrator login systems
- Password hashing
- Lesson booking, modification and cancellation
- Instructor availability management
- Student lesson history
- UK postcode validation
- Route and journey calculations using OpenRouteService
- Email-based OTP password resets
- Input validation and exception handling
- Instructor feedback and reports
- SQLite database storage for users, bookings and other system data

## Technologies Used

- Python
- CustomTkinter
- SQLite
- OpenRouteService API
- SMTP for email OTP functionality

## OpenRouteService API

This project uses the OpenRouteService API for route and travel calculations.

To run this functionality, you will need to create your own OpenRouteService account and generate an API key.

You can then add your API key to the relevant section of the program before running it.

The repository does not include my personal API key.

## Running the Project

1. Clone or download the repository.
2. Install the required Python libraries.
3. Add your OpenRouteService API key.
4. Configure the email details used for OTP password resets if you want to use that functionality.
5. Run the main Python file.

Some sample databases, reports or other resources may also be added separately to demonstrate the system.

## About the Project

The project was designed around the idea of a driving school needing one system for managing students, instructors and lessons.

Students can manage their bookings, instructors can control their availability and view their lessons, and administrators have access to wider management features.

Because this was originally an A Level project, there are parts of the code I would structure differently now. I have kept most of the original project intact while fixing issues and making improvements rather than completely rebuilding it.
