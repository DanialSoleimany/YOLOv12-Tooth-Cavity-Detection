#!/usr/bin/env python
# coding: utf-8

styles = """
<style>

.title {
  width: 100%;
  margin: 0 auto 25px auto;
  padding: 20px 10px;
  background-color: #6A0DAD;
  color: #FFD700;
  font-weight: bold;
  font-family: 'Century Gothic', sans-serif;
  font-size: clamp(16px, 3vw, 20px);  /* کوچکتر از قبل */
  text-align: center;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(106, 13, 173, 0.2);
}



/* === کانتینر معرفی === */
.about-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 25px 30px;
  border: 2px solid #B388EB;
  border-radius: 20px;
  background: linear-gradient(145deg, #F9F4FF, #F3E8FF);
  box-shadow: 0 8px 20px rgba(138, 43, 226, 0.15);
  text-align: center;
  font-family: 'Century Gothic', sans-serif;
  color: #4B0082;
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
  color: #6A0DAD;
  border: 2px solid #6A0DAD;
  border-radius: 25px;
  text-align: center;
  text-decoration: none !important;
  font-size: 13px;
  font-weight: bold;
  font-family: 'Century Gothic', sans-serif;
  transition: all 0.3s ease;
}
.fancy-button:hover {
  background-color: #6A0DAD;
  color: #FFD700 !important;
  transform: scale(1.05);
  text-decoration: none !important;
}
.button-row {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 20px;
}

/* === Table Of Contents === */
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
  background-color: #6A0DAD;
  color: #FFFFFF;
  font-weight: bold;
  font-size: 22px; 
  font-family: 'Century Gothic';
  width: auto;
  text-align: center;
}

/* === TOC Buttons === */
.button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 600px;
  height: 60px;
  margin: 10px auto;
  background-color: #9B59B6;
  color: #F8F1FF;
  border: none;
  border-radius: 50px;
  text-align: center;
  text-decoration: none;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Century Gothic';
  transition: transform 0.6s ease, background-position 0s ease, color 0.3s ease;
}
.button:hover {
  background-image: linear-gradient(to right, #8E44AD 0%, #6C3483 50%, #8E44AD 100%);
  background-size: 300% 100%;
  background-position: 100% 0%;
  transform: scale(1.1);
  color: #FFD700;
}

/* === Responsive (Mobile) === */
@media (max-width: 500px) {
  .fancy-button {
    width: 90%;
    font-size: 14px;
  }
  .button-row {
    flex-direction: column;
    align-items: center;
  }
  .button {
    width: 90%;
  }
}

</style>
"""
