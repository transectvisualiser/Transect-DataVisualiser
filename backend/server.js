require("dotenv").config();
const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { createClient } = require("@supabase/supabase-js");

const app = express();
app.use(cors());
app.use(express.json());

// Debugging: Ensure environment variables are loaded
console.log("SUPABASE_URL:", process.env.SUPABASE_URL);
console.log("SUPABASE_KEY:", process.env.SUPABASE_KEY ? "Loaded" : "Not Loaded");

if (!process.env.SUPABASE_URL || !process.env.SUPABASE_KEY) {
  console.error("Supabase environment variables are missing.");
  process.exit(1);
}

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

// Configure Multer for file uploads
const upload = multer({ storage: multer.memoryStorage() });

app.get("/", (req, res) => {
  res.send("Server is running!");
});

// Upload route
app.post("/upload", upload.single("image"), async (req, res) => {
  console.log("Upload Route Hit");

  try {
    if (!req.file) {
      console.log("No file received.");
      return res.status(400).json({ error: "No file uploaded" });
    }

    const file = req.file;
    const filePath = `visualizations/${Date.now()}_${file.originalname}`;

    console.log(`Uploading file: ${file.originalname} to Supabase at ${filePath}`);

    const { data, error } = await supabase.storage
      .from("visualizations")
      .upload(filePath, file.buffer, { contentType: file.mimetype });

    if (error) {
      console.error("Upload error:", error.message);
      return res.status(500).json({ error: error.message });
    }

    const publicUrl = supabase.storage.from("visualizations").getPublicUrl(filePath).data.publicUrl;
    console.log("Upload successful:", publicUrl);

    res.json({ message: "Upload successful", url: publicUrl });
  } catch (err) {
    console.error("Unexpected Upload failure:", err.message);
    res.status(500).json({ error: "Upload failed", details: err.message });
  }
});

// Fetch images route
app.get("/images", async (req, res) => {
    try {
        console.log("Fetching uploaded images...");
        
        const { data, error } = await supabase.storage.from("visualizations").list("visualizations");

        if (error) {
            console.error("Fetch error:", error.message);
            return res.status(500).json({ error: error.message });
        }

        // Construct full public URLs
        const imageUrls = data.map(file =>
            `https://${process.env.SUPABASE_URL.replace("https://", "")}/storage/v1/object/public/visualizations/visualizations/${file.name}`
        );

        console.log("Images fetched successfully:", imageUrls);
        res.json(imageUrls);
    } catch (err) {
        console.error("Failed to fetch images:", err.message);
        res.status(500).json({ error: "Failed to fetch images" });
    }
});


// Start the server
const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
