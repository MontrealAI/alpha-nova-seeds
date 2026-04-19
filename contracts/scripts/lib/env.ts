import "dotenv/config";
import { z } from "zod";

const envSchema = z.object({
  MAINNET_RPC_URL: z.string().url().optional(),
  MAINNET_RPC_URL_SECONDARY: z.string().url().optional(),
  MAINNET_FORK_RPC_URL: z.string().url().optional(),
  SEPOLIA_RPC_URL: z.string().url().optional(),
  ETHERSCAN_API_KEY: z.string().min(1).optional(),
  DEPLOYER_PRIVATE_KEY: z.string().min(1).optional(),
  DEPLOYMENT_CONFIG_PATH: z.string().min(1).optional(),
  ADMIN_OWNER_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/),
  PAUSER_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/).optional(),
  EMERGENCY_GUARDIAN_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/).optional(),
  TREASURY_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/).optional(),
  REVIEWER_REWARD_TREASURY_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/).optional(),
  COUNCIL_ADMIN_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/).optional(),
  ENS_REGISTRY_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/).optional(),
  NAMEWRAPPER_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/).optional(),
  ENS_NAME: z.string().min(1).optional(),
  AGI_TOKEN_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/),
  AGIJOBMANAGER_ADDRESS: z.string().regex(/^0x[a-fA-F0-9]{40}$/),
  ALLOW_DEPLOY_TO_SEPOLIA: z.enum(["true", "false"]).default("false"),
  ALLOW_DEPLOY_TO_MAINNET: z.enum(["true", "false"]).default("false"),
  ALLOW_OWNERSHIP_TRANSFER: z.enum(["true", "false"]).default("false"),
  ALLOW_ENS_PUBLISH: z.enum(["true", "false"]).default("false")
});

export type DeployEnv = z.infer<typeof envSchema>;

export function getEnv(): DeployEnv {
  const parsed = envSchema.safeParse(process.env);
  if (!parsed.success) {
    const details = parsed.error.issues
      .map((issue) => `- ${issue.path.join(".") || "env"}: ${issue.message}`)
      .join("\n");
    throw new Error(`Environment validation failed:\n${details}`);
  }
  return parsed.data;
}

export function assertSafetyFlag(flag: keyof Pick<DeployEnv, "ALLOW_DEPLOY_TO_MAINNET" | "ALLOW_DEPLOY_TO_SEPOLIA" | "ALLOW_OWNERSHIP_TRANSFER" | "ALLOW_ENS_PUBLISH">, context: string): void {
  const env = getEnv();
  if (env[flag] !== "true") {
    throw new Error(`${context} blocked: set ${flag}=true to continue.`);
  }
}
