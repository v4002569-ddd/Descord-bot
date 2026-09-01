import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

questions = [
    {
        "question": "أمامك موقف صعب، ماذا تفعل؟",
        "answers": [
            ("أواجهه بشجاعة", "gryffindor"),
            ("أبحث عن أفضل طريقة للفوز", "slytherin"),
            ("أفكر فيه بهدوء", "ravenclaw"),
            ("أطلب مساعدة أصدقائي", "hufflepuff")
        ]
    },
    {
        "question": "ما الصفة التي تهمك أكثر؟",
        "answers": [
            ("الشجاعة", "gryffindor"),
            ("الطموح", "slytherin"),
            ("الذكاء", "ravenclaw"),
            ("الوفاء", "hufflepuff")
        ]
    },
    {
        "question": "لو وجدت سرًا غامضًا في هوغوورتس، ماذا تفعل؟",
        "answers": [
            ("أدخل وأكتشفه", "gryffindor"),
            ("أستفيد منه لمصلحتي", "slytherin"),
            ("أبحث وأحل اللغز", "ravenclaw"),
            ("أخبر أصدقائي ونكتشفه معًا", "hufflepuff")
        ]
    },
    {
        "question": "أي مكان تفضّل في هوغوورتس؟",
        "answers": [
            ("ساحة التدريب", "gryffindor"),
            ("الزنزانة والغرف السرية", "slytherin"),
            ("المكتبة", "ravenclaw"),
            ("غرفة هافلباف", "hufflepuff")
        ]
    },
    {
        "question": "ماذا تفعل إذا تعرض صديقك لمشكلة؟",
        "answers": [
            ("أدافع عنه فورًا", "gryffindor"),
            ("أضع خطة ذكية لمساعدته", "slytherin"),
            ("أحل المشكلة بالتفكير", "ravenclaw"),
            ("أبقى بجانبه مهما حدث", "hufflepuff")
        ]
    }
]

house_names = {
    "gryffindor": "🦁 غريفندور",
    "slytherin": "🐍 سليذرين",
    "ravenclaw": "🦅 رافنكلو",
    "hufflepuff": "🦡 هافلباف"
}

scores = {}


class SortingView(discord.ui.View):
    def __init__(self, user, question_number):
        super().__init__(timeout=120)
        self.user = user
        self.question_number = question_number

        for answer, house in questions[question_number]["answers"]:
            button = discord.ui.Button(
                label=answer,
                style=discord.ButtonStyle.primary
            )

            async def callback(interaction, house=house):
                if interaction.user.id != self.user.id:
                    await interaction.response.send_message(
                        "هذه الأسئلة ليست لك 🎩",
                        ephemeral=True
                    )
                    return

                scores[self.user.id][house] += 1
                await interaction.response.defer()

                next_question = self.question_number + 1

                if next_question >= len(questions):
                    result = max(
                        scores[self.user.id],
                        key=scores[self.user.id].get
                    )

                    await interaction.edit_original_response(
                        content=(
                            f"🎩 **قبعة التصنيف قررت!**\n\n"
                            f"أنت تنتمي إلى **{house_names[result]}**!\n\n"
                            f"مبروك أيها الساحر ✨"
                        ),
                        view=None
                    )

                    del scores[self.user.id]
                    return

                await interaction.edit_original_response(
                    content=(
                        f"🎩 **السؤال {next_question + 1} من "
                        f"{len(questions)}**\n\n"
                        f"{questions[next_question]['question']}"
                    ),
                    view=SortingView(self.user, next_question)
                )

            button.callback = callback
            self.add_item(button)


@bot.event
async def on_ready():
    print(f"تم تشغيل قبعة التصنيف باسم {bot.user}")


@bot.command()
async def sorting(ctx):
    scores[ctx.author.id] = {
        "gryffindor": 0,
        "slytherin": 0,
        "ravenclaw": 0,
        "hufflepuff": 0
    }

    await ctx.send(
        f"🎩 **قبعة التصنيف**\n\n"
        f"أهلًا {ctx.author.mention}!\n"
        f"أجب عن الأسئلة التالية لأحدد المنزل المناسب لك.\n\n"
        f"**السؤال 1 من {len(questions)}**\n\n"
        f"{questions[0]['question']}",
        view=SortingView(ctx.author, 0)
    )


bot.run(os.getenv("TOKEN"))