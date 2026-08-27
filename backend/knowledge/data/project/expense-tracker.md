# Expense Tracker

A full expense-tracking ecosystem built across three apps sharing one backend API:
a React Native mobile app, a React web dashboard, and the API itself.

**Mobile** (expense-tracker-mobile): React Native with Expo SDK 55 and TypeScript.
JWT authentication with automatic session refresh, adding/viewing/removing expenses,
category selection via chips, spending breakdown via pie charts (react-native-chart-kit),
and secure credential storage with expo-secure-store.
GitHub: https://github.com/plamenzubev/expense-tracker-mobile

**Web dashboard** (expense-tracker-web): React + TypeScript, using Recharts for
visualization, Axios for API calls, and React Router DOM for navigation. Same core
feature set as the mobile app (JWT auth with refresh, CRUD on expenses, category
filtering and pie-chart breakdowns) in a responsive web interface.
GitHub: https://github.com/plamenzubev/expense-tracker-web

**API** (expense-tracker-api): a production-ready REST API built with Django and
Django REST Framework, PostgreSQL, and JWT auth via SimpleJWT (login, registration,
token refresh). Handles expense CRUD and globally shared expense categories, with CORS
configured for both the web and mobile clients, deployed on Render.
GitHub: https://github.com/plamenzubev/expense-tracker-api

An alternate implementation of the same API also exists in Node.js/TypeScript
(expense-tracker-api-node), built to compare a Node backend against the Django one for
the same feature set.
