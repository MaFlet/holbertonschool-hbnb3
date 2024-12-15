const express = require('express');
const mysql = require('mysql');
const bcrypt = require('bcrypt');
const cors = require('cors');
const session = require('express-session');
const { v4: uuidv4 } = require('uuid');
const app = express();


app.use(express.json());
app.use(cors({
    origin: 'http://localhost:5000',
    credentials: true
}));

app.use(session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: false,
        maxAge: 24 * 60 * 60 * 1000 // 24hours
    }
}));

// Database connection
const db = mysql.createConnection({
    host: "0.0.0.0",
    user: "hbnb_evo_2",
    password: "hbnb_evo_2_pwd",
    database: "hbnb_evo_2_db"
});

db.query(`
    ALTER TABLE users
    ADD COLUMN IF NOT EXISTS user_type ENUM('visitor', 'owner') DEFAULT 'visitor'
`);

// Register endpoint
app.post('/register', async (req, res) => {
    const { first_name, last_name, email, password, user_type } = req.body;

    try {
        // check if user already exists
        const [existingUsers] = await db.promise().query(
            'SELECT * FROM users WHERE email = ?',
            [email]
        );

        if (existingUsers.length > 0) {
            return res.status(400).json({ message: 'Email already registered' });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        const userId = uuidv4();

        // Inserting new user with user type
        await db.promise().query(
            'INSERT INTO users (id, first_name, last_name, email, password, user_type) VALUES (?, ?, ?, ?, ?, ?)',
            [userID, first_name, last_name, email, hashedPassword, user_type]
        );

        res.status(201).json({ message: 'User registered successfully!' });
    } catch (error) {
        console.error('Registration error:', error);
        res.status(500).json({ message: 'Server error' });
    }
});

// Login endpoint
app.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        //Find user
        const [users] = await db.promise().query(
            'SELECT * FROM users WHERE email = ?',
            [email]
        );
        if (users.length === 0) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }
        const user = users[0];

        //Compare password
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.status(401).json({ message: 'Invalid credentials '});
        }

        //Setting the session
        req.session.userId = user.id;
        req.session.userType = user.user_type;

        res.json({
            message: 'Login successful!',
            user: {
                id: user.id,
                first_name: user.first_name,
                last_name: user.last_name,
                email: user.email,
                userType: user.user_type
            }
        });
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ message: 'Server error' });
    }
});

//Getting user profile
app.get('/profile', async (req, res) => {
    if (!req.session.userId) {
        return res.status(401).json({ message: 'Not authenticated' });
    }
    
    try {
        const [users] = await db.promise().query(
            'SELECT id, first_name, last_name, email, user_type, created_at, updated_at FROM users WHERE id = ?',
            [req.session.userID]
        );
        if (users.length === 0) {
            return res.status(404).json({ message: 'User not found' });
        }

        res.json(users[0]);
    } catch (error) {
        console.error('Profile fetch error', error);
        res.status(500).json({ message: 'Server error' });
    }
});

// Check auth status endpoint
app.get('/check-auth', (req, res) => {
    if (req.session.userId) {
        res.json({ 
            authenticated: true,
            userType: req.session.userType
        });
    } else {
        res.json({ 
            authenticated: false,
            userType: null
        });
    }
});

// Start server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});