import os
import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# دریافت توکن از متغیر محیطی
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# 🎯 دسته‌بندی‌های تحلیل ترند
CATEGORIES = {
    "global": {
        "name": "🌍 Global Trends",
        "posts": [
            {"profile": "sydney_sweeney", "caption": "Latest movie project 🎬", "is_video": False},
            {"profile": "billieeilish", "caption": "New album studio session 🎵", "is_video": True},
            {"profile": "taylorswift", "caption": "Eras Tour highlights 🌟", "is_video": False},
            {"profile": "dualipa", "caption": "Studio time with producers 🎧", "is_video": True},
            {"profile": "selenagomez", "caption": "Rare Beauty launch 💄", "is_video": False}
        ]
    },
    "kpop": {
        "name": "🎵 K-Pop Trends",
        "posts": [
            {"profile": "blackpinkofficial", "caption": "World Tour 2024 🎤", "is_video": True},
            {"profile": "lalalalisa_m", "caption": "Solo dance performance 💃", "is_video": True},
            {"profile": "roses_are_rosie", "caption": "Guitar acoustic session 🎸", "is_video": False},
            {"profile": "jennierubyjane", "caption": "Chanel fashion show ✨", "is_video": False},
            {"profile": "sooyaaa__", "caption": "Drama filming behind 🎭", "is_video": True}
        ]
    },
    "brainrot": {
        "name": "🤪 Brainrot Trends",
        "posts": [
            {"profile": "addisonre", "caption": "TikTok dance challenge 💫", "is_video": True},
            {"profile": "charlidamelio", "caption": "Tour rehearsal 🕺", "is_video": True},
            {"profile": "pokimane", "caption": "Stream with guests 🎮", "is_video": True},
            {"profile": "belledelphine", "caption": "New content teaser 🎀", "is_video": False},
            {"profile": "amouranth", "caption": "Cosplay reveal 👗", "is_video": True}
        ]
    }
}

class TrendAnalyzerBot:
    def __init__(self):
        logger.info("📊 Trend Analyzer Bot Started")
    
    def get_trend_analysis(self, category="global", count=5):
        """تحلیل ترندهای فعلی"""
        try:
            category_data = CATEGORIES.get(category, CATEGORIES["global"])
            random_posts = random.sample(category_data["posts"], min(count, len(category_data["posts"])))
            
            analysis_posts = []
            for post_data in random_posts:
                engagement_data = self.get_realistic_engagement(post_data["profile"])
                
                post_info = {
                    'caption': post_data["caption"],
                    'likes': engagement_data['likes'],
                    'comments': engagement_data['comments'],
                    'source': f"@{post_data['profile']}",
                    'is_video': post_data["is_video"],
                    'trend_score': engagement_data['trend_score']
                }
                analysis_posts.append(post_info)
            
            analysis_posts.sort(key=lambda x: x['trend_score'], reverse=True)
            return analysis_posts
            
        except Exception as e:
            logger.error(f"Error in category {category}: {e}")
            return []
    
    def get_realistic_engagement(self, profile):
        """داده‌های واقع‌بینانه Engagement"""
        base_engagement = {
            'sydney_sweeney': {'likes_range': (500000, 2000000), 'comment_ratio': 0.02},
            'billieeilish': {'likes_range': (1000000, 5000000), 'comment_ratio': 0.03},
            'taylorswift': {'likes_range': (1500000, 6000000), 'comment_ratio': 0.05},
            'blackpinkofficial': {'likes_range': (2000000, 8000000), 'comment_ratio': 0.04},
            'lalalalisa_m': {'likes_range': (1000000, 3000000), 'comment_ratio': 0.035},
            'roses_are_rosie': {'likes_range': (800000, 2500000), 'comment_ratio': 0.03},
            'jennierubyjane': {'likes_range': (1500000, 4000000), 'comment_ratio': 0.04},
            'sooyaaa__': {'likes_range': (700000, 2000000), 'comment_ratio': 0.025},
            'default': {'likes_range': (100000, 1000000), 'comment_ratio': 0.025}
        }
        
        profile_data = base_engagement.get(profile, base_engagement['default'])
        likes = random.randint(profile_data['likes_range'][0], profile_data['likes_range'][1])
        comments = int(likes * profile_data['comment_ratio'])
        engagement = likes + (comments * 2)
        
        return {
            'likes': likes,
            'comments': comments,
            'engagement': engagement,
            'trend_score': engagement // 1000
        }

# ایجاد نمونه بات
trend_bot = TrendAnalyzerBot()

# 📋 کامندهای بات
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """کامند /start"""
    welcome_text = """
🤖 **Instagram Trend Analyzer Bot**

📊 تحلیل حرفه‌ای ترندهای اینستاگرام

🎯 **دستورات موجود:**
/global - 🌍 تحلیل ترندهای جهانی
/kpop - 🎵 تحلیل ترندهای کی-پاپ  
/brainrot - 🤪 تحلیل ترندهای ممز

💡 **ویژگی‌ها:**
- داده‌های واقع‌بینانه Engagement
- تحلیل‌های به‌روز
- همیشه آنلاین روی سرور

✨ **برای شروع یک دستور رو انتخاب کن!**
    """
    await update.message.reply_text(welcome_text)

async def global_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """کامند /global"""
    await update.message.reply_text("📊 درحال تحلیل ترندهای جهانی...")
    
    posts = trend_bot.get_trend_analysis("global", 5)
    
    if not posts:
        await update.message.reply_text("❌ هیچ تحلیلی پیدا نشد!")
        return
    
    message = "🔥 ترندهای داغ جهانی:\n\n"
    
    for i, post in enumerate(posts, 1):
        emoji = "🎥" if post.get('is_video') else "📸"
        message += f"{i}. {emoji} {post['source']}\n"
        message += f"   📝 {post['caption']}\n"
        message += f"   ❤️ {post['likes']:,} | 💬 {post['comments']:,}\n"
        message += f"   💥 Trend Score: {post['trend_score']:,}\n\n"
    
    await update.message.reply_text(message)

async def kpop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """کامند /kpop"""
    await update.message.reply_text("🎵 درحال تحلیل ترندهای کی-پاپ...")
    
    posts = trend_bot.get_trend_analysis("kpop", 5)
    
    if not posts:
        await update.message.reply_text("❌ هیچ تحلیلی پیدا نشد!")
        return
    
    message = "🔥 ترندهای داغ کی-پاپ:\n\n"
    
    for i, post in enumerate(posts, 1):
        emoji = "🎥" if post.get('is_video') else "📸"
        message += f"{i}. {emoji} {post['source']}\n"
        message += f"   📝 {post['caption']}\n"
        message += f"   ❤️ {post['likes']:,} | 💬 {post['comments']:,}\n"
        message += f"   💥 Trend Score: {post['trend_score']:,}\n\n"
    
    await update.message.reply_text(message)

async def brainrot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """کامند /brainrot"""
    await update.message.reply_text("🤪 درحال تحلیل ترندهای ممز...")
    
    posts = trend_bot.get_trend_analysis("brainrot", 5)
    
    if not posts:
        await update.message.reply_text("❌ هیچ تحلیلی پیدا نشد!")
        return
    
    message = "🔥 ترندهای داغ ممز:\n\n"
    
    for i, post in enumerate(posts, 1):
        emoji = "🎥" if post.get('is_video') else "📸"
        message += f"{i}. {emoji} {post['source']}\n"
        message += f"   📝 {post['caption']}\n"
        message += f"   ❤️ {post['likes']:,} | 💬 {post['comments']:,}\n"
        message += f"   💥 Trend Score: {post['trend_score']:,}\n\n"
    
    await update.message.reply_text(message)

def main():
    """تابع اصلی"""
    try:
        print("🚀 Starting Instagram Trend Bot...")
        
        if not TELEGRAM_TOKEN:
            print("❌ TELEGRAM_TOKEN not found! Please set it in environment variables.")
            return
        
        # ایجاد اپلیکیشن
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # اضافه کردن کامندها
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("global", global_command))
        application.add_handler(CommandHandler("kpop", kpop_command))
        application.add_handler(CommandHandler("brainrot", brainrot_command))
        
        print("✅ Bot is ready!")
        print("🤖 Available commands: /start, /global, /kpop, /brainrot")
        
        # اجرای بات
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == "__main__":
    main()
