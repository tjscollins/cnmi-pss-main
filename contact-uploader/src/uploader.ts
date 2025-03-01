import { rateLimit } from "./ajax/interceptors";

import Configuration from "./handlers/Configuration";
import Downloader from "./handlers/Downloader";
import Personnel from "./handlers/personnel";
import Offices from "./handlers/offices";
import Schools from "./handlers/schools";
import Headstarts from "./handlers/headstarts";


class Uploader {
    private config: Configuration

    constructor() {
        this.config = new Configuration("./contactUploader.json");
        this.upload = this.upload.bind(this);
    }

    public async run(): Promise<void> {
        const { config, upload } = this;

        if (config.rateLimit) {
            rateLimit(config.rateLimit);
        }
        if (config.download) {
            const downloader = new Downloader(config);
            await downloader.download();
        }
        if (config.all || config.personnel) await upload(Personnel);
        if (config.all || config.offices) await upload(Offices);
        if (config.all || config.schools) await upload(Schools);
        if (config.all || config.headstarts) await upload(Headstarts);
    }
    
    /**
     * Create a new instance of cls and use it to parse and post contact 
     * information to the WordPress site.
     * 
     * @param {*} cls 
     */
    private async upload(Cls: any) {
        const records = new Cls(this.config);

        await records.parse().catch((err) => {
            console.error(`Failed to parse ${Cls.name.toLowerCase()}\n`, err);
            console.log("Exiting...");
            process.exit(1);
        });
        await records.post().catch((err) => {
            console.error(`Failed to post ${Cls.name.toLowerCase()}\n`, err);
            console.log("Exiting...");
            process.exit(1);
        });
    }
}

export default Uploader;