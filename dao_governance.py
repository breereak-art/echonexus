"""
DAO Governance Module for EchoWorld Nexus
Enables decentralized mobility communities with NFT-based governance
"""

import os
import json
import hashlib
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict


POLYGON_MAINNET_RPC = "https://polygon-rpc.com"
POLYGON_MAINNET_CHAIN_ID = 137

POLYGON_AMOY_RPC = "https://rpc-amoy.polygon.technology"
POLYGON_AMOY_CHAIN_ID = 80002


@dataclass
class GovernanceProposal:
    """Represents a DAO governance proposal"""
    proposal_id: str
    title: str
    description: str
    proposal_type: str
    creator_address: str
    created_at: str
    voting_ends: str
    votes_for: int = 0
    votes_against: int = 0
    votes_abstain: int = 0
    status: str = "active"
    execution_data: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DAOMember:
    """Represents a DAO member with their NFT holdings"""
    address: str
    passport_nfts: List[str] = field(default_factory=list)
    voting_power: int = 0
    joined_at: str = field(default_factory=lambda: datetime.now().isoformat())
    proposals_created: int = 0
    votes_cast: int = 0
    reputation_score: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MobilityCommunity:
    """Represents a decentralized mobility community"""
    community_id: str
    name: str
    destination_country: str
    destination_city: str
    treasury_address: str
    members: List[DAOMember] = field(default_factory=list)
    proposals: List[GovernanceProposal] = field(default_factory=list)
    treasury_balance: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    governance_token: str = "ECHO"
    
    def to_dict(self) -> Dict:
        return {
            "community_id": self.community_id,
            "name": self.name,
            "destination_country": self.destination_country,
            "destination_city": self.destination_city,
            "treasury_address": self.treasury_address,
            "members": [m.to_dict() for m in self.members],
            "proposals": [p.to_dict() for p in self.proposals],
            "treasury_balance": self.treasury_balance,
            "created_at": self.created_at,
            "governance_token": self.governance_token
        }


class DAOGovernanceManager:
    """Manages DAO governance for mobility communities"""
    
    def __init__(self, use_mainnet: bool = False):
        self.use_mainnet = use_mainnet
        self.communities: Dict[str, MobilityCommunity] = {}
        self.member_registry: Dict[str, DAOMember] = {}
        
        self.rpc_url = POLYGON_MAINNET_RPC if use_mainnet else POLYGON_AMOY_RPC
        self.chain_id = POLYGON_MAINNET_CHAIN_ID if use_mainnet else POLYGON_AMOY_CHAIN_ID
    
    def create_community(
        self,
        name: str,
        destination_country: str,
        destination_city: str,
        creator_address: str
    ) -> MobilityCommunity:
        """Create a new mobility community DAO"""
        
        community_id = self._generate_id("community")
        treasury_address = self._generate_treasury_address(community_id)
        
        founder = self._get_or_create_member(creator_address)
        founder.voting_power = 100
        
        community = MobilityCommunity(
            community_id=community_id,
            name=name,
            destination_country=destination_country,
            destination_city=destination_city,
            treasury_address=treasury_address,
            members=[founder]
        )
        
        self.communities[community_id] = community
        return community
    
    def join_community(
        self,
        community_id: str,
        member_address: str,
        passport_nft_id: str = None
    ) -> Optional[DAOMember]:
        """Join a mobility community with optional NFT passport"""
        
        if community_id not in self.communities:
            return None
        
        community = self.communities[community_id]
        member = self._get_or_create_member(member_address)
        
        if passport_nft_id:
            member.passport_nfts.append(passport_nft_id)
            member.voting_power += self._calculate_voting_power(passport_nft_id)
        else:
            member.voting_power = 10
        
        if member.address not in [m.address for m in community.members]:
            community.members.append(member)
        
        return member
    
    def create_proposal(
        self,
        community_id: str,
        creator_address: str,
        title: str,
        description: str,
        proposal_type: str,
        voting_duration_days: int = 7,
        execution_data: Dict = None
    ) -> Optional[GovernanceProposal]:
        """Create a governance proposal"""
        
        if community_id not in self.communities:
            return None
        
        community = self.communities[community_id]
        
        member = next((m for m in community.members if m.address == creator_address), None)
        if not member:
            return None
        
        proposal_id = self._generate_id("proposal")
        voting_ends = (datetime.now() + timedelta(days=voting_duration_days)).isoformat()
        
        proposal = GovernanceProposal(
            proposal_id=proposal_id,
            title=title,
            description=description,
            proposal_type=proposal_type,
            creator_address=creator_address,
            created_at=datetime.now().isoformat(),
            voting_ends=voting_ends,
            execution_data=execution_data or {}
        )
        
        community.proposals.append(proposal)
        member.proposals_created += 1
        
        return proposal
    
    def cast_vote(
        self,
        community_id: str,
        proposal_id: str,
        voter_address: str,
        vote: str
    ) -> Dict[str, Any]:
        """Cast a vote on a proposal"""
        
        if community_id not in self.communities:
            return {"success": False, "error": "Community not found"}
        
        community = self.communities[community_id]
        proposal = next((p for p in community.proposals if p.proposal_id == proposal_id), None)
        
        if not proposal:
            return {"success": False, "error": "Proposal not found"}
        
        if proposal.status != "active":
            return {"success": False, "error": "Proposal voting has ended"}
        
        member = next((m for m in community.members if m.address == voter_address), None)
        if not member:
            return {"success": False, "error": "Not a community member"}
        
        voting_power = member.voting_power
        
        if vote == "for":
            proposal.votes_for += voting_power
        elif vote == "against":
            proposal.votes_against += voting_power
        elif vote == "abstain":
            proposal.votes_abstain += voting_power
        else:
            return {"success": False, "error": "Invalid vote option"}
        
        member.votes_cast += 1
        member.reputation_score += 1.0
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "vote": vote,
            "voting_power_used": voting_power,
            "current_results": {
                "for": proposal.votes_for,
                "against": proposal.votes_against,
                "abstain": proposal.votes_abstain
            }
        }
    
    def finalize_proposal(
        self,
        community_id: str,
        proposal_id: str
    ) -> Dict[str, Any]:
        """Finalize a proposal after voting ends"""
        
        if community_id not in self.communities:
            return {"success": False, "error": "Community not found"}
        
        community = self.communities[community_id]
        proposal = next((p for p in community.proposals if p.proposal_id == proposal_id), None)
        
        if not proposal:
            return {"success": False, "error": "Proposal not found"}
        
        total_votes = proposal.votes_for + proposal.votes_against + proposal.votes_abstain
        
        if proposal.votes_for > proposal.votes_against:
            proposal.status = "passed"
            execution_result = self._execute_proposal(proposal)
        else:
            proposal.status = "rejected"
            execution_result = None
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "final_status": proposal.status,
            "total_votes": total_votes,
            "votes_for": proposal.votes_for,
            "votes_against": proposal.votes_against,
            "votes_abstain": proposal.votes_abstain,
            "execution_result": execution_result
        }
    
    def get_community_stats(self, community_id: str) -> Dict[str, Any]:
        """Get statistics for a community"""
        
        if community_id not in self.communities:
            return {}
        
        community = self.communities[community_id]
        
        active_proposals = sum(1 for p in community.proposals if p.status == "active")
        passed_proposals = sum(1 for p in community.proposals if p.status == "passed")
        total_voting_power = sum(m.voting_power for m in community.members)
        
        return {
            "community_id": community_id,
            "name": community.name,
            "destination": f"{community.destination_city}, {community.destination_country}",
            "total_members": len(community.members),
            "total_proposals": len(community.proposals),
            "active_proposals": active_proposals,
            "passed_proposals": passed_proposals,
            "treasury_balance": community.treasury_balance,
            "total_voting_power": total_voting_power,
            "governance_token": community.governance_token
        }
    
    def _get_or_create_member(self, address: str) -> DAOMember:
        """Get existing member or create new one"""
        
        if address not in self.member_registry:
            self.member_registry[address] = DAOMember(address=address)
        return self.member_registry[address]
    
    def _calculate_voting_power(self, nft_id: str) -> int:
        """Calculate voting power based on NFT tier"""
        
        if "gold" in nft_id.lower():
            return 100
        elif "silver" in nft_id.lower():
            return 50
        elif "bronze" in nft_id.lower():
            return 25
        else:
            return 10
    
    def _generate_treasury_address(self, community_id: str) -> str:
        """Generate treasury address for community"""
        hash_value = hashlib.sha256(f"treasury_{community_id}".encode()).hexdigest()
        return f"0x{hash_value[:40]}"
    
    def _execute_proposal(self, proposal: GovernanceProposal) -> Dict:
        """Execute passed proposal"""
        
        return {
            "executed": True,
            "proposal_type": proposal.proposal_type,
            "execution_time": datetime.now().isoformat(),
            "message": f"Proposal '{proposal.title}' has been executed successfully"
        }
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID"""
        return f"{prefix}_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}"


def prepare_mainnet_nft_mint(
    wallet_address: str,
    metadata: Dict,
    use_mainnet: bool = False
) -> Dict[str, Any]:
    """
    Prepare NFT minting transaction for mainnet or testnet
    
    Args:
        wallet_address: User's wallet address
        metadata: NFT metadata
        use_mainnet: Whether to use mainnet
        
    Returns:
        Transaction preparation data
    """
    
    if use_mainnet:
        chain_config = {
            "chain_name": "Polygon Mainnet",
            "chain_id": POLYGON_MAINNET_CHAIN_ID,
            "rpc_url": POLYGON_MAINNET_RPC,
            "explorer": "https://polygonscan.com",
            "opensea": "https://opensea.io",
            "currency": "MATIC"
        }
    else:
        chain_config = {
            "chain_name": "Polygon Amoy Testnet",
            "chain_id": POLYGON_AMOY_CHAIN_ID,
            "rpc_url": POLYGON_AMOY_RPC,
            "explorer": "https://amoy.polygonscan.com",
            "opensea": "https://testnets.opensea.io",
            "currency": "MATIC (Testnet)"
        }
    
    estimated_gas = 150000
    estimated_gas_price = 30
    estimated_cost_matic = (estimated_gas * estimated_gas_price) / 1e9
    
    return {
        "to": wallet_address,
        "chain": chain_config,
        "metadata": metadata,
        "metadata_json": json.dumps(metadata, indent=2),
        "gas_estimate": {
            "gas_limit": estimated_gas,
            "gas_price_gwei": estimated_gas_price,
            "estimated_cost_matic": estimated_cost_matic,
            "estimated_cost_usd": estimated_cost_matic * 0.85
        },
        "instructions": {
            "step1": f"Connect your Web3 wallet to {chain_config['chain_name']}",
            "step2": f"Ensure you have {estimated_cost_matic:.4f} MATIC for gas",
            "step3": "Approve the transaction in your wallet",
            "step4": f"View your NFT on {chain_config['opensea']}"
        },
        "mainnet_warning": "MAINNET: Real MATIC will be spent!" if use_mainnet else None
    }


def get_dao_proposal_types() -> List[Dict[str, str]]:
    """Get available proposal types"""
    
    return [
        {
            "id": "treasury_allocation",
            "name": "Treasury Allocation",
            "description": "Propose how to spend community treasury funds"
        },
        {
            "id": "community_guidelines",
            "name": "Community Guidelines",
            "description": "Propose changes to community rules and guidelines"
        },
        {
            "id": "partnership",
            "name": "Partnership Proposal",
            "description": "Propose partnerships with service providers or other communities"
        },
        {
            "id": "member_spotlight",
            "name": "Member Spotlight",
            "description": "Nominate members for recognition and rewards"
        },
        {
            "id": "resource_sharing",
            "name": "Resource Sharing",
            "description": "Propose shared resources like housing tips, job leads, etc."
        },
        {
            "id": "governance_change",
            "name": "Governance Change",
            "description": "Propose changes to voting rules or governance structure"
        }
    ]


_dao_manager = None

def get_dao_manager(use_mainnet: bool = False) -> DAOGovernanceManager:
    """Get or create singleton DAO manager"""
    global _dao_manager
    if _dao_manager is None or _dao_manager.use_mainnet != use_mainnet:
        _dao_manager = DAOGovernanceManager(use_mainnet=use_mainnet)
    return _dao_manager


def create_demo_community(country: str, city: str) -> MobilityCommunity:
    """Create a demo community for testing"""
    
    manager = get_dao_manager(use_mainnet=False)
    
    demo_address = "0x" + "1" * 40
    
    community = manager.create_community(
        name=f"{city} Global Movers DAO",
        destination_country=country,
        destination_city=city,
        creator_address=demo_address
    )
    
    manager.join_community(community.community_id, "0x" + "2" * 40, "gold_passport_001")
    manager.join_community(community.community_id, "0x" + "3" * 40, "silver_passport_002")
    manager.join_community(community.community_id, "0x" + "4" * 40, "bronze_passport_003")
    
    manager.create_proposal(
        community_id=community.community_id,
        creator_address=demo_address,
        title="Welcome Package for New Members",
        description="Create a welcome package with local tips and resources for new members moving to the city.",
        proposal_type="resource_sharing"
    )
    
    return community
