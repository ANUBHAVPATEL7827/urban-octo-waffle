# 🛠️ Job Alert Telegram Bot

A 24/7 bot that scrapes job listings (SarkariResult, etc.) and posts to Telegram channels.

## 🔧 Features

- Auto scrape jobs and post to channels
- Manual /postjob command
- Admin-only channel management
- Error logging & modular code

## ⚙️ Deploy

1. Click the button below:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?templateUrl=https://github.com/YOUR_USERNAME/YOUR_REPO)

2. Set Environment Variables:
   - `BOT_TOKEN` → Your bot token
   - `ADMIN_ID` → Your Telegram user ID

3. Done!

## 🧠 Commands

- `/postjob Title | Description | Link`
- `/addchannel @channelusername`
- `/removechannel @channelusername`
- `/listchannels`
