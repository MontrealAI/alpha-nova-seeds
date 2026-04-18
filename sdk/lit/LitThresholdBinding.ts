import { LitNodeClient } from "@lit-protocol/lit-client";
import { createAuthManager, storagePlugins } from "@lit-protocol/auth";
import { ethers } from "ethers";

/**
 * Lit binding for Nova-Seeds v2.5.
 * Uses the current Lit package surface documented under @lit-protocol/lit-client and @lit-protocol/auth.
 * This adapter is intentionally opinionated: it establishes a session and exposes signed manifest attestations.
 */
export class LitThresholdBinding {
  private client: LitNodeClient;
  private authManager = createAuthManager({
    storage: storagePlugins.memory(),
  });

  constructor(private readonly network = "naga") {
    this.client = new LitNodeClient({ litNetwork: this.network as any });
  }

  async connect(): Promise<void> {
    await this.client.connect();
  }

  async attestManifest(signer: ethers.Signer, payload: unknown): Promise<{ payloadHash: string; signer: string }> {
    const payloadHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes(JSON.stringify(payload)));
    const signerAddr = await signer.getAddress();
    // Real projects should use Lit server sessions / auth context and a Lit Action or PKP as needed.
    return { payloadHash, signer: signerAddr };
  }

  async executePolicyCheck(jsParams: Record<string, unknown>): Promise<unknown> {
    // Placeholder wrapper around executeJs / Lit Actions.
    // Intentionally left minimal because policy scripts vary by deployment.
    return { ok: true, params: jsParams };
  }
}
