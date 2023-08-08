from main import app, db
from flask import render_template, redirect, url_for, flash, request
from main.models import Customer, Order, Product
from datetime import datetime, timedelta
import calendar
