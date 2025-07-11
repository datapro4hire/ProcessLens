# ProcessLens

Advanced Enterprise Content Management (ECM) plugin with GitHub OAuth authentication and PostgreSQL database integration.

## Features

- 🔐 **GitHub OAuth Authentication** - Secure login using GitHub accounts
- 📊 **User Management** - Store and manage user data in PostgreSQL
- 🎨 **Modern UI** - Beautiful, responsive interface with Bootstrap 5
- 📁 **Document Management** - Upload, organize, and search documents
- 🔄 **Workflow Automation** - Streamline business processes
- 🛡️ **Security & Compliance** - Enterprise-grade security features

## Tech Stack

- **Backend**: Flask, Flask-Dance (OAuth), Flask-SQLAlchemy
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, Font Awesome
- **Authentication**: GitHub OAuth 2.0

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- GitHub account (for OAuth setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ProcessLens
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb processlens
   ```

4. **Configure environment variables**
   ```bash
   # Copy example environment file
   cp env.example .env
   
   # Edit .env with your configuration
   nano .env
   ```

5. **Set up GitHub OAuth**
   - Go to [GitHub Developer Settings](https://github.com/settings/developers)
   - Create a new OAuth App
   - Set Authorization callback URL to: `http://localhost:5000/login/authorized`
   - Copy Client ID and Client Secret to your `.env` file

6. **Initialize the database**
   ```bash
   python init_db.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   - Open your browser to `http://localhost:5000`
   - Click "Login with GitHub" to authenticate

## Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/processlens

# GitHub OAuth Configuration
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

## Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| github_username | String(80) | GitHub username |
| github_id | Integer | GitHub user ID |
| access_token | Text | GitHub OAuth access token |
| created_at | DateTime | Account creation timestamp |
| updated_at | DateTime | Last update timestamp |

## API Endpoints

- `GET /` - Home page
- `GET /login` - Redirect to GitHub OAuth
- `GET /login/authorized` - OAuth callback handler
- `GET /dashboard` - User dashboard (requires authentication)
- `GET /logout` - Logout user

## Development

### Project Structure

```
ProcessLens/
├── app.py              # Main Flask application
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── env.example        # Environment variables template
├── templates/         # HTML templates
│   ├── base.html     # Base template
│   ├── index.html    # Home page
│   └── dashboard.html # User dashboard
└── README.md         # This file
```

### Running in Development

```bash
# Set debug mode
export FLASK_ENV=development

# Run with auto-reload
python app.py
```

### Database Migrations

The application uses SQLAlchemy for database management. Tables are created automatically when the app starts.

## Security Considerations

- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Store sensitive environment variables securely
- Regularly rotate GitHub OAuth tokens
- Implement proper session management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
