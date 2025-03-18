import pikepdf
pdf = pikepdf.open("linux_docker.pdf", password="/This is where ur password must be putted./")
pdf.save("unlocked.pdf")