import discord
from discord.ext import commands
import os
import pytesseract
from pdf2image import convert_from_path
import pikepdf
import itertools
import string
import asyncio
import tempfile

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='pdf ', intents=intents, help_command=None)

# Temporary directory for processing files
TEMP_DIR = "temp_files"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.command(name='help')
async def help_command(ctx):
    help_text = """
**PDF Processing Bot Commands**
`pdf ocr` - Extract text from a PDF file using OCR
`pdf unlock <password>` - Unlock a password-protected PDF
`pdf bruteforce` - Attempt to unlock a PDF using brute force
`pdf help` - Show this help message

For all commands that process PDFs, attach the PDF file to your message.
    """
    await ctx.send(help_text)

@bot.command(name='ocr')
async def ocr_command(ctx):
    if not ctx.message.attachments:
        await ctx.send("Please attach a PDF file to process!")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith('.pdf'):
        await ctx.send("Please attach a PDF file!")
        return

    await ctx.send("Processing PDF... This may take a while.")
    
    # Download the PDF
    temp_pdf_path = os.path.join(TEMP_DIR, attachment.filename)
    await attachment.save(temp_pdf_path)
    
    try:
        # Convert PDF to images
        images = convert_from_path(temp_pdf_path)
        extracted_text = ""
        
        # Process each page
        for i, img in enumerate(images):
            extracted_text += f"Page {i+1}:\n{pytesseract.image_to_string(img)}\n"
            extracted_text += "=" * 50 + "\n"
        
        # Save extracted text
        text_filename = attachment.filename.rsplit('.', 1)[0] + "_extracted.txt"
        text_path = os.path.join(TEMP_DIR, text_filename)
        
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        
        # Send the result
        await ctx.send("Text extraction completed!", file=discord.File(text_path))
        
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
    finally:
        # Cleanup
        try:
            os.remove(temp_pdf_path)
            os.remove(text_path)
        except:
            pass

@bot.command(name='unlock')
async def unlock_command(ctx, password: str):
    if not ctx.message.attachments:
        await ctx.send("Please attach a PDF file to unlock!")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith('.pdf'):
        await ctx.send("Please attach a PDF file!")
        return

    await ctx.send("Attempting to unlock PDF...")
    
    # Download the PDF
    temp_pdf_path = os.path.join(TEMP_DIR, attachment.filename)
    await attachment.save(temp_pdf_path)
    
    try:
        # Attempt to unlock the PDF
        pdf = pikepdf.open(temp_pdf_path, password=password)
        unlocked_filename = "unlocked_" + attachment.filename
        unlocked_path = os.path.join(TEMP_DIR, unlocked_filename)
        pdf.save(unlocked_path)
        
        # Send the unlocked PDF
        await ctx.send("PDF unlocked successfully!", file=discord.File(unlocked_path))
        
    except pikepdf.PasswordError:
        await ctx.send("Incorrect password!")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
    finally:
        # Cleanup
        try:
            os.remove(temp_pdf_path)
            os.remove(unlocked_path)
        except:
            pass

@bot.command(name='bruteforce')
async def bruteforce_command(ctx):
    if not ctx.message.attachments:
        await ctx.send("Please attach a PDF file to unlock!")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith('.pdf'):
        await ctx.send("Please attach a PDF file!")
        return

    await ctx.send("Starting brute force attempt... This may take a while.")
    
    # Download the PDF
    temp_pdf_path = os.path.join(TEMP_DIR, attachment.filename)
    await attachment.save(temp_pdf_path)
    
    try:
        # Bruteforce attempt
        characters = string.ascii_letters + string.digits
        found = False
        
        status_message = await ctx.send("Trying passwords...")
        
        for length in range(1, 5):  # Try passwords of length 1 to 4
            if found:
                break
                
            await status_message.edit(content=f"Trying {length}-character passwords...")
            
            for password_tuple in itertools.product(characters, repeat=length):
                password = ''.join(password_tuple)
                try:
                    pdf = pikepdf.open(temp_pdf_path, password=password)
                    unlocked_filename = "unlocked_" + attachment.filename
                    unlocked_path = os.path.join(TEMP_DIR, unlocked_filename)
                    pdf.save(unlocked_path)
                    
                    await ctx.send(f"Password found: `{password}`")
                    await ctx.send("Here's your unlocked PDF:", file=discord.File(unlocked_path))
                    
                    found = True
                    break
                except pikepdf.PasswordError:
                    continue
        
        if not found:
            await ctx.send("Failed to find the password. Try longer passwords or use the manual unlock command.")
            
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
    finally:
        # Cleanup
        try:
            os.remove(temp_pdf_path)
            if found:
                os.remove(unlocked_path)
        except:
            pass

# Run the bot
if __name__ == "__main__":
    # Get the token from .env file
    from dotenv import load_dotenv
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if not TOKEN:
        print("Error: No token found in .env file!")
        exit(1)
        
    bot.run(TOKEN) 