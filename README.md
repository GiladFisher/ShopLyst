# ShopLyst

This project is a full-stack web application that allows users to create, categorize, and manage a list of grocery items. The app is built using:

- **Frontend**: React.js for the user interface.
- **Backend**: Flask for handling API requests and business logic.
- **Database**: Firebase for storing and retrieving data.

---

## Features

1. **Frontend (React)**
   - Users can input item details such as title, category, and description.
   - Items are auto-sorted by category for better organization.
   - Responsive and styled with CSS for a polished user experience.

2. **Backend (Flask)**
   - Receives and processes requests from the React frontend.
   - Interacts with Firebase to store and retrieve data.
   - Provides intelligent suggestions for item categories based on the title.

3. **Firebase Integration**
   - Secure and scalable storage solution.
   - Handles persistent data for the application.

---

## Project Structure

```
/ShopLyst
├── /client         # React app
    |-/my-react-app
│    ├── public        # Static files
│    ├── src           # React components and logic
│    ├── package.json  # Frontend dependencies
├── /server/Python API          # Flask backend
│   ├── model_sorter.py        # Main Flask app
│   ├── requirements.txt  # Backend dependencies
├── README.md         # Project documentation
```

---

## Requirements

- **Node.js** (for React)
- **Python 3.x** (for Flask)
- Firebase account and credentials

---

## Setup Instructions

### Frontend (React)
1. Navigate to the `client/my-react-app` folder:
   ```bash
   cd client/my-react-app
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Build for production:
   ```bash
   npm run build
   ```

### Backend (Flask)
1. Navigate to the `server/Python API` folder:
   ```bash
   cd server/Python\ API
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```bash
   python model_sorter.py
   ```

---

## Deployment

### Frontend
1. Deploy the React app as a static site (e.g., Render or Netlify).
2. Use the `client/my-react-app/build` directory as the publish directory.

### Backend
1. Deploy the Flask app as a web service (e.g., Render or Heroku).
2. Set environment variables for Firebase credentials.

---

## Usage
1. Access the deployed React app in your browser.
2. Add items using the provided form.
3. View and manage your list, sorted by category.

---

## Future Enhancements
- Real-time data updates using Firebase listeners.
- User authentication for personalized lists.
- Improved categorization using machine learning.

---

## License
This project is licensed under the MIT License.

