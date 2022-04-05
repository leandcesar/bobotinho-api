# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only, validates
from sqlalchemy.event import listens_for

db = SQLAlchemy()
