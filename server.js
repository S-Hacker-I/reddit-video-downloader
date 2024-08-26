const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(express.static('public'));

// Route to serve the HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/download', (req, res) => {
    const videoUrl = req.body.videoUrl;
    const outputDir = path.resolve(__dirname, 'public');

    const getMetadataCommand = `yt-dlp --get-filename -o "%(title)s.%(ext)s" "${videoUrl}"`;

    exec(getMetadataCommand, (error, stdout) => {
        if (error) {
            console.error(`Error getting metadata: ${error.message}`);
            res.status(500).json({ error: 'Failed to get video metadata' });
            return;
        }

        const originalName = stdout.trim();
        const outputFilePath = path.resolve(outputDir, originalName);

        const downloadCommand = `yt-dlp -f "bestvideo+bestaudio[ext=m4a]/best[ext=mp4]/best" "${videoUrl}" -o "${outputFilePath}"`;

        exec(downloadCommand, (downloadError) => {
            if (downloadError) {
                console.error(`Error downloading video: ${downloadError.message}`);
                res.status(500).json({ error: 'Failed to download video' });
                return;
            }

            res.json({ filePath: `/${originalName}`, originalName });
        });
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
