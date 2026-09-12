# ISS Tracker

A small Python script that tells you **the next time the International Space Station
(ISS) will be visible from your location** — enter your latitude, longitude and
elevation, and it computes the next visible pass and how long it will last.

## Features

- Computes the **next visible ISS pass** for any location on Earth
- Reports the **date, time and duration** of the pass
- Uses live orbital data via [`pyephem`](https://rhodesmill.org/pyephem/)

## Requirements

- Python 3
- [`requests`](https://pypi.org/project/requests/)
- [`pyephem`](https://pypi.org/project/pyephem/)

```bash
pip install requests pyephem
```

## Usage

```bash
python main.py
```

The script prompts for your location as `latitude, longitude, elevation`:

```
Enter the location you desire (format: latitude, longitude, elevation): 47.04936, 8.30519, 450
The ISS will be visible from Lucerne on 2022-04-09 20:15:52 for 6 minutes
```

## Contributing

Contributions are welcome — open an issue or submit a pull request.

## License

Free to use and modify.
