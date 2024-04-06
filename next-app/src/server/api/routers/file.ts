import S3 from "aws-sdk/clients/s3";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";
import { z } from "zod";
import { randomUUID } from "crypto";


const s3 = new S3({
  apiVersion: "2006-03-01",
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.BUCKET_REGION,
  signatureVersion: "v4",
});

type presignedPostOut = { 
  url: string;
  key: string;
}

export const fileRouter = createTRPCRouter({
  create: publicProcedure
    .input(z.object({ name: z.string().min(1) }))
    .mutation(async ({ ctx, input }) => {

      return ctx.db.post.create({
        data: {
          name: input.name,
        },
      });
    }),

  getSignedUrl: publicProcedure.input(z.object({ name: z.string().min(1), type: z.string(),folder: z.string().min(1) }))
  .mutation(async({ input }): Promise<presignedPostOut> =>  {

    const Key = `${input.folder}/${randomUUID()}-${input.name}`

    const s3Params = {
      Bucket: "ragtestnextgpt",
      Key,
      Expires: 60,
      // ContentType: `image/${ex}`,
    };

    // eslint-disable-next-line @typescript-eslint/await-thenable
    const uploadUrl = await s3.getSignedUrl("putObject", s3Params);
    const presignedPostresp = { url: uploadUrl, key: Key };
    console.log(" returning url: ", uploadUrl)

    return presignedPostresp;
  }),
});
