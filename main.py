import os
import logging
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from pydub import AudioSegment
from pedalboard import Pedalboard, NoiseGate, Compressor, Reverb, HighpassFilter, Gain, Chorus, Limiter
from pedalboard.io import AudioFile

# إعدادات المراقبة
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# التوكن الصحيح الخاص بك
TOKEN = "8679718692:AAHngR8g2vR04Xt925e8Qw5wT6VWj2rEejY"

# أنماط الاستوديو
PRESETS = {
    "tarab": {"name": "🎙️ نمط الطرب والشرقي", "chain": [NoiseGate(threshold_db=-38), HighpassFilter(cutoff_frequency_hz=100), Compressor(threshold_db=-16, ratio=2.5), Reverb(room_size=0.6, wet_level=0.3), Limiter(threshold_db=-1.0), Gain(gain_db=2)]},
    "rap": {"name": "🎧 نمط الراب والبوب", "chain": [NoiseGate(threshold_db=-32), Compressor(threshold_db=-14, ratio=4), Chorus(), Limiter(threshold_db=-0.5), Gain(gain_db=3)]},
    "podcast": {"name": "📻 نمط البودكاست", "chain": [NoiseGate(threshold_db=-45), Compressor(threshold_db=-20, ratio=3.5), Limiter(threshold_db=-2.0), Gain(gain_db=5)]},
    "clean": {"name": "✨ تنقية احترافية", "chain": [NoiseGate(threshold_db=-40), HighpassFilter(cutoff_frequency_hz=95), Gain(gain_db=1)]}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"✅ استلام أمر البداية من: {update.effective_user.first_name}")
    user_name = html.escape(update.effective_user.first_name)
    
    welcome_text = (
        f"أهلاً بك يا فنان <b>{user_name}</b> في استوديو <b>Manix</b>! 🌟\n\n"
        "أرسل لي الآن تسجيلك الصوتي أو ملفاً صوتياً لنبدأ السحر!"
    )
    
    # تصحيح الخطأ: تم تغيير callback_query_data إلى callback_data
    keyboard = [[InlineKeyboardButton("📖 دليل الاستخدام", callback_data='help')]]
    
    await update.message.reply_text(
        welcome_text, 
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode='HTML'
    )

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        await query.edit_message_text(
            "💡 <b>نصيحة:</b> سجل في مكان هادئ للحصول على أفضل نقاوة صوت.",
            parse_mode='HTML'
        )
    elif query.data.startswith('proc_'):
        preset_key = query.data.replace('proc_', '')
        await query.edit_message_text(f"⏳ جاري تطبيق نمط <b>{PRESETS[preset_key]['name']}</b>...", parse_mode='HTML')
        # [تتم هنا عملية المعالجة]

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🎵 استلام ملف صوتي...")
    file_id = update.message.voice.file_id if update.message.voice else update.message.audio.file_id
    context.user_data['file'] = file_id
    
    # تصحيح كافة الأزرار هنا أيضاً
    keyboard = [[InlineKeyboardButton(v["name"], callback_data=f"proc_{k}")] for k, v in PRESETS.items()]
    await update.message.reply_text(
        "<b>✅ وصل الإبداع!</b> اختر النمط الآن:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_query_handler))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))

    print("🚀 البوت يعمل الآن بدون أخطاء.. جربه!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
