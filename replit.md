# Tap to Win Pro - Professional Clicker Game

## Overview

This is a comprehensive professional clicker web application featuring rupee currency, achievements system, power-ups, detailed statistics tracking, and modern responsive design. The game includes advanced features like floating animations, haptic feedback, achievement unlocking, multiplier system, and persistent game state. Built as a static web application using vanilla HTML, CSS, and JavaScript, served via Python's built-in HTTP server.

## System Architecture

### Frontend Architecture
- **Technology**: Vanilla HTML5, CSS3, and JavaScript with API integration
- **Design Pattern**: Single-page application (SPA) with server-side data persistence
- **UI Framework**: Custom CSS with gradient backgrounds and modern styling
- **Responsive Design**: Mobile-first approach with viewport meta tag and flexible layouts
- **Data Flow**: Hybrid approach with server-first storage and localStorage fallback

### Backend Architecture
- **Server**: FastAPI with Uvicorn serving both static files and REST API
- **Database**: PostgreSQL with persistent player data storage
- **Port**: 5000 (configurable)
- **API Endpoints**: RESTful API for player data, leaderboard, and game state management
- **Data Persistence**: Server-side database with automatic migration from localStorage

## Key Components

### Core Files
1. **index.html**: Complete professional clicker game application
   - Professional header with navigation and stats toggle
   - Advanced stats panel with click tracking, session time, and performance metrics
   - Achievement system with 4 unlockable achievements
   - Power-up system with 4 purchasable multipliers (2x to 25x)
   - Enhanced money display with shimmer animations
   - Floating number animations on clicks
   - Reset functionality with confirmation
   - Professional footer with branding
   - Leaderboard modal for competitive gameplay

2. **server.py**: FastAPI backend server
   - RESTful API endpoints for player data management
   - PostgreSQL database integration
   - Player creation, save/load, and reset operations
   - Leaderboard functionality with top 10 players
   - Static file serving for the frontend

3. **generated-icon.png**: Custom favicon for the application

### Game Features
- **Statistics Tracking**: Total clicks, click rate per minute, session time, best streak
- **Achievement System**: 4 achievements (First Steps, Getting Rich, Millionaire, Click Master)
- **Power-Up System**: 4 tiers of multipliers that stack multiplicatively
- **Visual Effects**: Floating numbers, shimmer animations, click animations
- **Notifications**: Achievement unlock notifications with slide animations
- **Database Integration**: PostgreSQL storage with automatic localStorage migration
- **Leaderboard System**: Competitive ranking of top 10 players by earnings
- **Mobile Optimization**: Touch events, haptic feedback, responsive design
- **Professional UI**: Header/footer navigation, stats panels, modern styling

## Data Flow

1. **Hybrid Data Storage**: Primary storage in PostgreSQL database with localStorage fallback
2. **Server-First Architecture**: Game state synchronizes with server on every save operation
3. **API Communication**: RESTful endpoints for player data, save/load operations, and leaderboards
4. **Real-time Updates**: Game updates happen through JavaScript DOM manipulation with server persistence
5. **Automatic Migration**: Existing localStorage data automatically migrates to server storage

## External Dependencies

### Runtime Dependencies
- **Python 3.11**: For serving static files
- **Node.js 20**: Listed in modules but not currently used
- **No external libraries**: Vanilla JavaScript implementation

### Development Environment
- **Replit**: Cloud-based development environment
- **Nix**: Package management (stable-24_05 channel)

## Deployment Strategy

### Local Development
- Python HTTP server on port 5000
- Parallel workflow execution in Replit
- Hot reload through browser refresh

### Production Deployment
- Static file hosting compatible
- Can be deployed to any web server or CDN
- No server-side processing required
- Minimal resource requirements

### Scalability Considerations
- Pure client-side means infinite horizontal scalability
- No database bottlenecks
- CDN-friendly for global distribution

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

## Recent Changes

### June 21, 2025 - Professional Enhancement Update
- **Enhanced Visual Design**: Upgraded to glassmorphism design with Inter font, improved color gradients, and premium visual effects
- **Advanced Performance Tracking**: Added real-time performance metrics, click delay analysis, and efficiency scoring
- **Enterprise-Level Features**: 
  - Real-time player ranking with percentile calculation
  - Enhanced milestone notifications with custom animations
  - Click ripple effects and haptic feedback patterns
  - Connection status monitoring with offline/online indicators
- **Professional UI/UX**:
  - Redesigned header with brand identity and status indicators
  - Enhanced button interactions with advanced hover states
  - Improved responsive design with accessibility features (dark mode, reduced motion, high contrast)
  - Professional typography and spacing improvements
- **Backend Enhancements**:
  - Added comprehensive API endpoints for global statistics and player rankings
  - Enhanced leaderboard with player status tracking (online/recent/offline)
  - Improved error handling and logging with FastAPI
  - Added CORS middleware and professional API documentation

## Changelog
- June 21, 2025: Initial setup and professional enhancement to enterprise-level standards