Its a flask application.
To run in local just do
<code>flask run</code>

To build docker image do
<code>docker build --tag benford_flask .</code>

To run
<code>docker run -i -p 5000:5000 -d benford_flask</code>