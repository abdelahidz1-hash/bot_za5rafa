import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import fal_client

# إعدادات التوكن والمفتاح
TELEGRAM_TOKEN = "7989116766:AAHuvR5MYs8geGczCWCpAm22Vq8fLa4pnoc"
FAL_API_KEY = "Fal_sk_6a70dd262d944321a03a01e5ec73ffd2:a19fc8634974f10894e2eb0fb1975eef"

# تعيين مفتاح Fal.ai في المتغيرات البيئية ليعمل مع مكتبة fal_client تلقائياً
os.environ["FAL_KEY"] = FAL_API_KEY

# إعداد البوت والمستقبلات
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "أهلاً بك يا عبد الله! ✨\n"
        "أنا بوت تصميم الفيديوهات بالذكاء الاصطناعي عبر Fal.ai.\n"
        "أرسل لي الآن وصفاً نصياً (Prompt) باللغة الإنجليزية لما تريد تصميمه وسأقوم بتحويله إلى فيديو فوراً!"
    )

@dp.message()
async def generate_video_handler(message: types.Message):
    prompt_text = message.text
    
    # إرسال رسالة للمستخدم بأن العملية قيد التنفيذ
    status_msg = await message.answer("⏳ جاري توليد الفيديو بالذكاء الاصطناعي، يرجى الانتظار قليلاً (قد يستغرق بعض الوقت)...")
    
    try:
        # تشغيل طلب توليد الفيديو عبر Fal.ai باستخدام نموذج Kling Video Turbo
        # ملاحظة: يمكنك تغيير اسم الموديل حسب رغبتك من موقع fal.ai
        handler = fal_client.submit(
            "fal-ai/kling-video/v3/turbo/pro/text-to-video",
            arguments={
                "prompt": prompt_text
            }
        )
        
        # انتظار واستلام النتيجة
        result = handler.get()
        video_url = result["video"]["url"]
        
        # إرسال الفيديو الناتج للمستخدم
        await message.answer_video(
            video=video_url, 
            caption=f"✨ **تم إنشاء الفيديو بنجاح!**\n📝 الوصف: {prompt_text}"
        )
        
    except Exception as e:
        await message.answer(f"❌ حدث خطأ أثناء توليد الفيديو:\n`{str(e)}`")
        
    finally:
        # حذف رسالة الانتظار
        try:
            await status_msg.delete()
        except:
            pass

async def main():
    print("🤖 البوت يعمل الآن ويستمع للرسائل...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
