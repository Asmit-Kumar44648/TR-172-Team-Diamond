"use client";

import { useMemo } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, PerspectiveCamera, Html } from "@react-three/drei";
import { GraspRecord } from "@/lib/types";

interface ThreeViewerProps {
  mode: '3d' | 'seg' | 'depth';
  grasps: GraspRecord[];
  selectedIndex: number | null;
  onSelectGrasp: (index: number | null) => void;
}

function GraspObject({ grasp, index, isSelected, onSelect }: { grasp: GraspRecord, index: number, isSelected: boolean, onSelect: (i: number) => void }) {
  const g = grasp.grasp;
  const isRejected = grasp.rejected;
  const isOperational = grasp.is_operational;
  
  const color = isRejected ? "#ef4444" : isOperational ? "#22c55e" : "#6366f1";
  const size = isRejected || isOperational ? 0.008 : 0.004;

  return (
    <group position={[g.position.x, g.position.y, g.position.z]}>
      <mesh onClick={() => onSelect(index)} onPointerOver={() => document.body.style.cursor = 'pointer'} onPointerOut={() => document.body.style.cursor = 'auto'}>
        <sphereGeometry args={[size, 16, 16]} />
        <meshStandardMaterial 
          color={color} 
          emissive={color} 
          emissiveIntensity={isSelected ? 2 : 0.5} 
        />
      </mesh>
      
      {(isRejected || isOperational || isSelected) && (
        <Html distanceFactor={0.5} position={[0, size + 0.01, 0]}>
          <div className={`px-2 py-0.5 rounded-sm text-[8px] font-bold whitespace-nowrap shadow-lg border ${
            isRejected ? "bg-red-950/90 border-red-500 text-red-100" : 
            isOperational ? "bg-green-950/90 border-green-500 text-green-100" : 
            "bg-zinc-950/90 border-zinc-700 text-zinc-100"
          }`}>
            {isRejected ? "❌ REJECTED" : isOperational ? "✓ OPERATIONAL" : `#${grasp.rank}`}
          </div>
        </Html>
      )}

      {/* Approach/Retreat arrows placeholder */}
      {isSelected && (
        <group>
          <mesh position={[0, 0, -0.015]} rotation={[Math.PI/2, 0, 0]}>
            <cylinderGeometry args={[0.0005, 0.0005, 0.03]} />
            <meshBasicMaterial color="#6366f1" />
          </mesh>
        </group>
      )}
    </group>
  );
}

export default function ThreeViewer({ mode, grasps, selectedIndex, onSelectGrasp }: ThreeViewerProps) {
  if (mode !== '3d') {
    return (
      <div className="flex-1 flex items-center justify-center bg-zinc-950 font-mono text-zinc-600 text-[10px] uppercase">
        {mode} view currently rendering...
      </div>
    );
  }

  return (
    <div className="absolute inset-0">
      <Canvas shadows dpr={[1, 2]}>
        <color attach="background" args={["#0d0d0f"]} />
        <PerspectiveCamera makeDefault position={[0.5, 0.5, 0.5]} fov={45} />
        <OrbitControls makeDefault rotateSpeed={0.5} zoomSpeed={0.8} minDistance={0.1} maxDistance={2} enableDamping={false} />
        
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <gridHelper args={[1, 10, "#18181b", "#18181b"]} rotation={[Math.PI/2, 0, 0]} />
        
        {/* Grasp objects */}
        {grasps.map((g, i) => (
          <GraspObject 
            key={g.grasp.grasp_id} 
            grasp={g} 
            index={i} 
            isSelected={selectedIndex === i} 
            onSelect={onSelectGrasp}
          />
        ))}

        {/* Shadow floor for scale */}
        <mesh rotation={[-Math.PI/2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
          <planeGeometry args={[2, 2]} />
          <shadowMaterial opacity={0.3} />
        </mesh>
      </Canvas>
    </div>
  );
}
