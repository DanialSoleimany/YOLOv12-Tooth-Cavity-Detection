#!/usr/bin/env python
# coding: utf-8

styles = """
<style>

.title {
  width: 100%;
  margin: 0 auto 25px auto;
  padding: 20px 10px;
  background-color: #0A0F2C;
  color: #4AC4FF;
  font-weight: bold;
  font-family: 'Century Gothic', sans-serif;
  font-size: clamp(16px, 3vw, 20px);
  text-align: center;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(74, 196, 255, 0.25);
}

/* === کانتینر معرفی === */
.about-container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 25px 30px;
  border: 2px solid #8B4D9C;
  border-radius: 20px;
  background: linear-gradient(145deg, #0A0F2C, #1B123A);
  box-shadow: 0 8px 20px rgba(74, 196, 255, 0.1);
  text-align: center;
  font-family: 'Century Gothic', sans-serif;
  color: #F8F8FF;
  box-sizing: border-box;
}
.about-container p {
  font-size: 16px;
  line-height: 1.6;
}
.about-container b {
  font-size: 18px;
}

/* === دکمه‌ها (fancy-button) === */
.fancy-button {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 130px;
  height: 55px;
  margin: 8px;
  background-color: transparent;
  color: #FFA500;
  border: 2px solid #FFA500;
  border-radius: 25px;
  text-align: center;
  text-decoration: none !important;
  font-size: 13px;
  font-weight: bold;
  font-family: 'Century Gothic', sans-serif;
  transition: all 0.3s ease;
}
.fancy-button:hover {
  background-color: #FFA500;
  color: #0A0F2C !important;
  transform: scale(1.05);
  text-decoration: none !important;
}

/* === Additional Fancy Buttons for Plum and Cyan === */
.fancy-button.plum {
  border-color: #D176C4;
  color: #D176C4;
}
.fancy-button.plum:hover {
  background-color: #D176C4;
  color: #0A0F2C !important;
}
.fancy-button.cyan {
  border-color: #4AC4FF;
  color: #4AC4FF;
}
.fancy-button.cyan:hover {
  background-color: #4AC4FF;
  color: #0A0F2C !important;
}

/* === Button Row (centered default) === */
.button-row {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 20px;
}

/* === NEW: Button Row aligned to right === */
.button-row.right {
  justify-content: flex-end;
  padding-right: 20px;
}

/* === Table Of Contents Label === */
.text-container {
  text-align: center;
  font-size: 12px;
  margin: 5px;
  padding: 5px;
}
.text {
  display: inline-block;
  padding: 20px 60px; 
  border-top-left-radius: 60px;
  border-top-right-radius: 30px;
  border-bottom-right-radius: 60px;
  border-bottom-left-radius: 30px;
  background-color: #4AC4FF;
  color: #0A0F2C;
  font-weight: bold;
  font-size: 22px; 
  font-family: 'Century Gothic';
  width: 100%;
  text-align: center;
  box-sizing: border-box;
}

/* === TOC Container === */
.toc-container {
  background: linear-gradient(145deg, #0A0F2C, #1B123A);
  border: 2px solid #4AC4FF;
  border-radius: 20px;
  padding: 20px;
  width: 100%;
  max-width: 100%;
  margin: 0;
  box-shadow: 0 4px 20px rgba(74, 196, 255, 0.15);
  box-sizing: border-box;
}

/* === TOC Buttons (Blue Style w/ hover fix) === */
.button {
  display: block;
  width: 70%;
  margin: 10px auto;
  padding: 14px 24px;
  background-color: #0A0F2C;
  color: #4AC4FF;
  border: 2px solid #4AC4FF;
  border-radius: 50px;
  text-align: center;
  font-size: 16px;
  font-weight: bold;
  font-family: 'Century Gothic', sans-serif;
  transition: all 0.3s ease;
  text-decoration: none !important;
}
.button:hover {
  background-color: #4AC4FF;
  color: #0A0F2C !important;
  transform: scale(1.05);
  text-decoration: none !important;
}
.button:visited {
  color: #4AC4FF;
  text-decoration: none !important;
}

/* === Responsive (Mobile) === */
@media (max-width: 500px) {
  .fancy-button {
    width: 90%;
    font-size: 14px;
  }
  .button-row,
  .button-row.right {
    flex-direction: column;
    align-items: center;
  }
  .button {
    width: 90%;
  }
}

</style>
"""






