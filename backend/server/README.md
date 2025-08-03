# 🚀 LunaLens Backend Server

<div align="center">

![LunaLens Backend](https://img.shields.io/badge/LunaLens-Backend-blue?style=for-the-badge&logo=server)
![Flask](https://img.shields.io/badge/Flask-API-red?style=for-the-badge&logo=flask)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange?style=for-the-badge&logo=sqlalchemy)
![JWT](https://img.shields.io/badge/JWT-Auth-purple?style=for-the-badge&logo=jwt)
![SQLite](https://img.shields.io/badge/SQLite-Database-yellow?style=for-the-badge&logo=sqlite)

<br>

<div style="background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 20px; margin: 25px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">

# 🌙 **Advanced AI-Powered Lunar Surface Analysis System**

*A comprehensive backend server with database integration, user management, and advanced analytics for lunar surface analysis.*

</div>

<br>

[![Stars](https://img.shields.io/github/stars/your-repo/lunalens-backend?style=social)](https://github.com/your-repo/lunalens-backend)
[![Forks](https://img.shields.io/github/forks/your-repo/lunalens-backend?style=social)](https://github.com/your-repo/lunalens-backend)
[![Issues](https://img.shields.io/github/issues/your-repo/lunalens-backend)](https://github.com/your-repo/lunalens-backend/issues)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🌟 **Features**

<div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🎯 **Core Capabilities**

<table>
<tr>
<td align="center" width="50%">

#### 🤖 **AI-Powered Analysis**
- 🔍 **Boulder Detection**: Advanced AI models for lunar object detection
- 📊 **Analytics**: Comprehensive analysis tracking and reporting
- 🎨 **Visualization**: Grad-CAM and detection visualizations
- 📈 **Metrics**: Detailed performance and accuracy metrics

</td>
<td align="center" width="50%">

#### 🛡️ **Security & Authentication**
- 🔐 **JWT Authentication**: Secure token-based authentication system
- 👥 **User Management**: Multi-user support with role-based access
- 🔒 **File Security**: Secure file upload and storage
- 🛡️ **API Protection**: RESTful API with comprehensive security

</td>
</tr>
<tr>
<td align="center" width="50%">

#### 💾 **Database Integration**
- 🗄️ **SQLAlchemy ORM**: Advanced database management
- 📊 **SQLite Support**: Built-in database (no installation required)
- 🐘 **PostgreSQL Ready**: Production-ready database support
- 📈 **Analytics**: Comprehensive data tracking and reporting

</td>
<td align="center" width="50%">

#### 🔧 **System Features**
- 📁 **File Management**: Secure file upload and storage
- 📊 **Logging**: Comprehensive system logging
- 🔄 **API Endpoints**: Complete RESTful API
- 📈 **Monitoring**: Real-time system monitoring

</td>
</tr>
</table>

</div>

---

## 📋 **Prerequisites**

<div style="background: linear-gradient(45deg, #ff6b35, #f7931e); padding: 15px; border-radius: 10px; margin: 10px 0;">

- 🐍 **Python 3.8+** (Tested with Python 3.13)
- 🗄️ **SQLite** (Built into Python - no installation required)
- 🖥️ **Node.js** (for frontend integration)

</div>

---

## 🛠️ **Installation**

<div style="background: linear-gradient(45deg, #4facfe, #00f2fe); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🚀 **Step 1: Clone the Repository**

```bash
git clone <repository-url>
cd lunalens/backend/server
```

### 📦 **Step 2: Install Dependencies**

```bash
# Install basic dependencies (recommended for Windows)
pip install Flask Flask-CORS Flask-SQLAlchemy Flask-Migrate PyJWT python-dotenv Werkzeug numpy opencv-python Pillow

# Or install from requirements.txt (if available)
pip install -r requirements.txt
```

### 🗄️ **Step 3: Database Setup**

#### 🗄️ **SQLite Database (Default - No Installation Required)**
The system uses SQLite by default, which is built into Python and requires no additional installation.

#### 🐘 **PostgreSQL Database (Optional - For Production)**
If you prefer PostgreSQL for production:

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

#### 🔧 **Create Database and User (PostgreSQL only)**

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create user and database
CREATE USER lunalens WITH PASSWORD 'lunalens123';
CREATE DATABASE lunalens_db OWNER lunalens;
CREATE DATABASE lunalens_dev OWNER lunalens;
CREATE DATABASE lunalens_test OWNER lunalens;

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE lunalens_db TO lunalens;
GRANT ALL PRIVILEGES ON DATABASE lunalens_dev TO lunalens;
GRANT ALL PRIVILEGES ON DATABASE lunalens_test TO lunalens;

# Exit PostgreSQL
\q
```

### ⚙️ **Step 4: Environment Configuration**

```bash
# Copy environment example
cp env.example .env

# Edit .env file with your configuration (optional for SQLite)
# For SQLite, the default configuration will work
```

### 🗄️ **Step 5: Initialize Database**

```bash
# Run the database setup script
python setup_database.py

# This will:
# - Create all database tables
# - Initialize demo users
# - Create logs directory
# - Set up the complete system
```

</div>

---

## 🏃‍♂️ **Running the Server**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🚀 **Development Mode**

```bash
python app.py
```

### 🏭 **Production Mode**

```bash
# Set environment
set FLASK_CONFIG=production  # Windows
export FLASK_CONFIG=production  # Linux/macOS

# Run with gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

</div>

---

## 📊 **Database Schema**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🗄️ **Core Tables**

#### 👥 **Users**
- `id`: Primary key
- `mission_id`: Unique mission identifier
- `name`: User display name
- `role`: User role (admin, user, researcher)
- `permissions`: JSON array of permissions
- `created_at`: Account creation timestamp
- `last_login`: Last login timestamp
- `is_active`: Account status

#### 📊 **Analyses**
- `id`: Primary key
- `user_id`: Foreign key to users
- `analysis_type`: Type of analysis (basic, advanced, full)
- `image_filename`: Original image filename
- `image_path`: Full path to uploaded image
- `processing_time`: Analysis duration in seconds
- `status`: Analysis status (pending, processing, completed, failed)
- `created_at`: Analysis creation timestamp
- `updated_at`: Last update timestamp
- `total_objects`: Number of detected objects
- `boulder_count`: Number of boulders detected
- `crater_count`: Number of craters detected
- `average_confidence`: Average confidence score
- `average_diameter`: Average object diameter
- `average_area`: Average object area
- `total_volume`: Total volume of all objects
- `average_circularity`: Average circularity score
- `average_elongation`: Average elongation score
- `visualization_path`: Path to detection visualization
- `gradcam_path`: Path to Grad-CAM visualization

#### 🎯 **Detected Objects**
- `id`: Primary key
- `analysis_id`: Foreign key to analyses
- `object_index`: Order in detection sequence
- `class_name`: Object class (boulder, crater, etc.)
- `confidence`: Detection confidence score
- `degradation_state`: Object degradation state
- `width_real`: Real width in meters
- `height_real`: Real height in meters
- `diameter_real`: Real diameter in meters
- `area_real`: Real area in square meters
- `volume_real`: Real volume in cubic meters
- `estimated_depth`: Estimated depth in meters
- `circularity`: Circularity score
- `elongation`: Elongation score
- `bounding_box`: JSON bounding box coordinates
- `pixel_measurements`: JSON pixel measurements

#### 📈 **Density Analysis**
- `id`: Primary key
- `analysis_id`: Foreign key to analyses
- `total_area`: Total image area in square meters
- `crater_density`: Craters per square meter
- `boulder_density`: Boulders per square meter
- `overall_density`: Total objects per square meter

#### 🔄 **Analysis Sessions**
- `id`: Primary key
- `user_id`: Foreign key to users
- `session_id`: Unique session identifier
- `started_at`: Session start timestamp
- `completed_at`: Session completion timestamp
- `status`: Session status (active, completed, failed)
- `analysis_count`: Number of analyses in session

#### 📝 **System Logs**
- `id`: Primary key
- `timestamp`: Log timestamp
- `level`: Log level (INFO, WARNING, ERROR, DEBUG)
- `category`: Log category (auth, analysis, system, etc.)
- `message`: Log message
- `user_id`: Associated user (optional)
- `analysis_id`: Associated analysis (optional)
- `additional_data`: JSON additional context

</div>

---

## 🔌 **API Endpoints**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🔐 **Authentication**
- `POST /login` - User login
- `POST /logout` - User logout
- `POST /verify-token` - Verify JWT token

### 📊 **Analytics**
- `GET /api/analytics/summary` - Get analytics summary
- `GET /api/analyses` - Get all analyses (paginated)
- `GET /api/analyses/<id>` - Get specific analysis details

### 🪨 **Boulder Detection**
- `POST /api/boulder/upload` - Upload image for analysis
- `POST /api/boulder/analyze` - Analyze uploaded image
- `GET /api/boulder/status` - Check system status

### 📁 **File Serving**
- `GET /uploads/<filename>` - Serve uploaded files

</div>

---

## 🔐 **Authentication**

<div style="background: linear-gradient(45deg, #ffecd2, #fcb69f); padding: 20px; border-radius: 15px; margin: 20px 0;">

The system uses JWT (JSON Web Tokens) for authentication:

### 🔄 **Authentication Flow**

1. 🚪 **Login**: User provides mission_id and access_code
2. 🔑 **Token Generation**: Server generates JWT with user info
3. ✅ **Token Verification**: All protected endpoints verify JWT
4. ⏰ **Token Expiration**: Tokens expire after 24 hours

### 👥 **Demo Users**

<table>
<tr>
<th>🚀 Mission ID</th>
<th>🔑 Access Code</th>
<th>👤 Role</th>
<th>🎯 Access Level</th>
</tr>
<tr>
<td><code>isro123</code></td>
<td><code>isro123@2024</code></td>
<td>👑 Admin</td>
<td>🟢 Full Access</td>
</tr>
<tr>
<td><code>mission001</code></td>
<td><code>mission001@2024</code></td>
<td>👤 Mission Team</td>
<td>🟡 Standard Access</td>
</tr>
<tr>
<td><code>research002</code></td>
<td><code>research002@2024</code></td>
<td>🔬 Research Team</td>
<td>🔵 Research Access</td>
</tr>
<tr>
<td><code>test001</code></td>
<td><code>test001@2024</code></td>
<td>🧪 Test User</td>
<td>🟠 Test Access</td>
</tr>
</table>

</div>

---

## 📈 **Analytics Features**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 📊 **Dashboard Analytics**
- 📈 Total analyses performed
- 👥 Total users registered
- 📅 Recent analyses (last 7 days)
- 🏆 Top users by analysis count

### 🔍 **Analysis Tracking**
- 📋 Complete analysis history
- 🎯 Object detection details
- ⏱️ Processing time metrics
- 📊 User activity patterns

### 📊 **System Monitoring**
- 📝 Comprehensive logging
- ❌ Error tracking
- ⚡ Performance metrics
- 👤 User session monitoring

</div>

---

## ⚙️ **Configuration**

<div style="background: linear-gradient(45deg, #4facfe, #00f2fe); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🔧 **Environment Variables**
- `FLASK_CONFIG`: Environment (development, production, testing)
- `DATABASE_URL`: Database connection string (SQLite default)
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT signing key
- `LOG_LEVEL`: Logging level
- `UPLOAD_FOLDER`: File upload directory

### 🗄️ **Database Configuration**
- **Development**: `sqlite:///lunalens_dev.db` (SQLite)
- **Production**: `sqlite:///lunalens.db` (SQLite)
- **Testing**: `sqlite:///lunalens_test.db` (SQLite)
- **PostgreSQL**: `postgresql://user:pass@localhost/dbname` (Optional)

</div>

---

## 🛡️ **Security Features**

<div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 20px; border-radius: 15px; margin: 20px 0;">

- 🔐 **JWT Authentication**: Secure token-based auth
- 🔒 **Password Hashing**: Secure credential storage
- 🌐 **CORS Protection**: Cross-origin request control
- 📁 **File Validation**: Upload file type checking
- 🛡️ **SQL Injection Protection**: SQLAlchemy ORM
- 🧹 **XSS Protection**: Input sanitization

</div>

---

## 📝 **Logging**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 20px; border-radius: 15px; margin: 20px 0;">

The system provides comprehensive logging:

- 🔐 **Authentication Events**: Login/logout tracking
- 🔍 **Analysis Events**: Processing start/completion
- ❌ **Error Tracking**: Detailed error logging
- ⚡ **Performance Metrics**: Processing time tracking
- 👤 **User Activity**: User action monitoring

</div>

---

## 🧪 **Testing**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🚀 **Quick Setup Test**

```bash
# Test server functionality
python test_server.py
```

### 🗄️ **Database Management**

```bash
# Check database connection
python setup_database.py --check

# Show database information
python setup_database.py --info

# Reset database (WARNING: deletes all data)
python setup_database.py --reset
```

### 🔌 **API Tests**

```bash
# Test authentication
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"missionId": "test001", "accessCode": "test001@2024"}'

# Test analysis
curl -X POST http://localhost:5000/api/boulder/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"filepath": "uploads/test.jpg", "analysisType": "basic"}'
```

</div>

---

## 🚀 **Deployment**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🛠️ **Development Setup**

1. 📦 Install Python dependencies
2. 🗄️ Run `python setup_database.py`
3. 🚀 Start server with `python app.py`
4. 🌐 Access at http://localhost:5000

### 🏭 **Production Setup**

1. ⚙️ Set `FLASK_CONFIG=production`
2. 🗄️ Configure production database (SQLite or PostgreSQL)
3. 🔐 Set secure secret keys
4. 🔒 Enable HTTPS
5. 🌐 Configure reverse proxy (nginx)
6. 📊 Set up monitoring and logging

### 🐳 **Docker Deployment**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

</div>

---

## 📞 **Support**

<div style="background: linear-gradient(45deg, #ffecd2, #fcb69f); padding: 20px; border-radius: 15px; margin: 20px 0;">

For issues and questions:
- 📝 Check the logs in `logs/lunalens.log`
- 🗄️ Review database connection settings
- ⚙️ Verify environment variables
- 🧪 Test with demo credentials
- 🔍 Run `python test_server.py` for diagnostics

</div>

---

## 🔄 **Database Migrations**

<div style="background: linear-gradient(45deg, #4facfe, #00f2fe); padding: 20px; border-radius: 15px; margin: 20px 0;">

When updating the database schema:

```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

</div>

---

## 📊 **Performance Optimization**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 20px; border-radius: 15px; margin: 20px 0;">

- 🗄️ **Database Indexing**: Optimized queries
- 🔄 **Connection Pooling**: Efficient database connections
- 🚀 **Caching**: Redis integration (optional)
- 📦 **File Compression**: Optimized file storage
- ⚡ **Async Processing**: Background task processing

</div>

---

## 🐛 **Troubleshooting**

<div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 20px; border-radius: 15px; margin: 20px 0;">

### ❌ **Common Issues**

#### 🐍 **Python 3.13 Compatibility**
- Some ML packages may not be compatible with Python 3.13
- Use Python 3.11 or 3.12 for full ML functionality
- Basic server functionality works with Python 3.13

#### 🗄️ **Database Issues**
- SQLite files are created automatically
- Check file permissions for database directory
- Use `python setup_database.py --check` to verify connection

#### 📦 **Package Installation Issues**
- Install packages individually if requirements.txt fails
- Use `pip install --upgrade pip` to update pip
- Some packages may require Visual Studio Build Tools on Windows

#### 🚀 **Server Not Starting**
- Check if port 5000 is available
- Verify all dependencies are installed
- Check logs in `logs/lunalens.log`

</div>

---

## 🔄 **Migration from PostgreSQL to SQLite**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; margin: 20px 0;">

If you were using PostgreSQL and want to switch to SQLite:

1. ⚙️ **Update config.py**: Change database URLs to SQLite
2. 🔧 **Update .env**: Set SQLite database URLs
3. 🗄️ **Run setup**: `python setup_database.py`
4. 🧪 **Test**: `python test_server.py`

</div>

---

## 📈 **Future Enhancements**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 20px; border-radius: 15px; margin: 20px 0;">

- 🐘 **PostgreSQL Support**: Full PostgreSQL integration
- 🤖 **ML Package Support**: Complete ML functionality
- 📊 **Advanced Analytics**: Enhanced reporting features
- ⚡ **Real-time Processing**: WebSocket support
- ☁️ **Cloud Deployment**: AWS/Azure integration

</div>

---

<div align="center">

## 🌙 **Happy Lunar Analysis!** 🚀

*LunaLens Backend Server - Advanced lunar surface analysis with comprehensive data management.*

<br>

[![Made with Love](https://img.shields.io/badge/Made%20with-Love-red?style=for-the-badge)](https://github.com/your-repo/lunalens-backend)
[![Powered by Flask](https://img.shields.io/badge/Powered%20by-Flask-red?style=for-the-badge)](https://flask.palletsprojects.com/)
[![Lunar Science](https://img.shields.io/badge/Lunar-Science-purple?style=for-the-badge)](https://github.com/your-repo/lunalens-backend)

</div> 