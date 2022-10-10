# Run
python3 main.py

# Compiling
pyinstaller main.spec</br>
You can now run the executable located at: dist/main.exe

# How does it work?
Uses image recognition to detect Q pop, and champ select pick/ban.

# Features
<ul>
  <li>Auto accept Q</li>
  <li>Auto lock in specific champ</li>
  <li>Auto ban specific champ</li>
  <li>Auto lock in and ban will only happen if the user has been idle (not moved their mouse) for 5 seconds or more</li>
  <li>If your selected pick/ban is not possible to pick/ban (eg. already picked or banned), nothing will automatically be picked/banned - there is no fallback, so relying on this feature could cause you to dodge!</li>
</ul>