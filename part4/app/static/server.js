const express = require('express');
const mysql = require('mysql');
const { v4: uuid} = require('uuid');

const app = express();

const connection = mysql.createConnection({
    host: "0.0.0.0",
    user: "hbnb_evo_2",
    password: "hbnb_evo_2_pwd",
    database: "hbnb_evo_2_db"
});

app.use(express.urlencoded({ extended: true }));

app.post('/register-visitor', (req, res) => {
    const { firstName, lastName, email, password } = req.body;
    const userID = uuid();

    connection.query(
        'INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (?, ?, ?, ?, ?, ?)',
        [userID, firstName, lastName, email, password, false],
        (error, result) => {
            if (error) {
                console.error('Error saving visitor:', error);
                return res.status(500).json({ message: 'Registration failed' + error.message });
            }
            return res.status(200).json({ message: 'Registration successful' });
        }
    );
});

app.listen(3000, () => {
    console.log('Server is running on port 5000');
});
