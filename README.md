# Secure Encrypted Database System

## Project Overview
The Secure Encrypted Database System is a robust solution designed to provide secure data storage and management. It offers insert, search, update, and delete operations with a role-based access control system, ensuring that only authorized users can access sensitive information.

## Features
- **Data Security**: Utilizes ECC (Elliptic Curve Cryptography) and AES (Advanced Encryption Standard) for data encryption, ensuring high levels of security.
- **Role-Based Access Control**: Implements a role-based system to manage user access to various functionalities of the database.
- **Data Operations**: Supports core database operations including insert, search, update, and delete.
- **User-Friendly Interface**: Provides a simplified interface for both developers and users.

## System Architecture
The system is structured to separate data management and security features, utilizing:
- **Client-Server Model**: The database operates on a client-server architecture, allowing remote access.
- **Encryption Module**: A dedicated module handles all encryption and decryption processes.
- **Access Control Layer**: Manages user roles and permissions, ensuring secure operations.

## Installation Instructions
1. Clone the repository:
   ```
   git clone https://github.com/Sirapxt/CSS454-and-CSS451-project.git
   ```
2. Navigate to the project directory:
   ```
   cd CSS454-and-CSS451-project
   ```
3. Install required dependencies:
   ```
   npm install
   ```
4. Configure the database connection settings in the `config.json` file.
5. Run the application:
   ```
   npm start
   ```

## Usage Examples
- **Inserting Data**:
   ```
   insertData(user, data);
   ```
- **Searching for Data**:
   ```
   searchData(query);
   ```
- **Updating Data**:
   ```
   updateData(userId, newData);
   ```
- **Deleting Data**:
   ```
   deleteData(userId);
   ```

## Development Information
- **Languages & Frameworks**: This project is developed using JavaScript, Node.js, and various libraries for encryption.
- **Contribution Guidelines**: Contributions are welcome! Please read the `CONTRIBUTING.md` file for guidelines.
- **License**: This project is licensed under the MIT License. See the `LICENSE` file for details.